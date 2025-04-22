from typing import Union, List, Dict, Optional
from openai import OpenAI

from .steps._1_get_entities import get_entities
from .steps._2_get_relations import get_relations
from .steps._3_cluster_graph import cluster_graph
from .utils.chunk_text import chunk_text
from .models import Graph
import dspy
import json
import os
from concurrent.futures import ThreadPoolExecutor
  
class KGGen:
  def __init__(
    self,
    model: str = "openai/gpt-4o",
    temperature: float = 0.0,
    api_key: str = None,
    api_base: str = None,
    model_type: str = None,
  ):
    """Initialize KGGen with optional model configuration
    
    Args:
        model: Name of model to use (e.g. 'gpt-4')
        temperature: Temperature for model sampling
        api_key: API key for model access
        api_base: API base URL for custom endpoints (e.g. SGLang server)
        model_type: Model type (e.g. 'chat' for SGLang)
    """
    self.dspy = dspy
    self.model = model
    self.temperature = temperature
    self.api_key = api_key
    self.api_base = api_base
    self.model_type = model_type
    self.init_model(model, temperature, api_key, api_base, model_type)
      
  def init_model(
    self,
    model: str = None,
    temperature: float = None,
    api_key: str = None,
    api_base: str = None,
    model_type: str = None,
  ):
    """Initialize or reinitialize the model with new parameters
    
    Args:
        model: Name of model to use (e.g. 'gpt-4')
        temperature: Temperature for model sampling
        api_key: API key for model access
        api_base: API base URL for custom endpoints (e.g. SGLang server)
        model_type: Model type (e.g. 'chat' for SGLang)
    """
    # Update instance variables if new values provided
    if model is not None:
      self.model = model
    if temperature is not None:
      self.temperature = temperature
    if api_key is not None:
      self.api_key = api_key
    if api_base is not None:
      self.api_base = api_base
    if model_type is not None:
      self.model_type = model_type
      
    # Initialize dspy LM with current settings
    if self.api_base and self.model_type:
      # 使用 SGLang 部署的 LLM
      # SGLang 部署的 LLM 不需要温度参数
      self.lm = dspy.LM(
        model=self.model, 
        api_key="local", 
        api_base=self.api_base,
        model_type=self.model_type
      )
    elif self.api_key:
      # 使用标准 OpenAI API
      self.lm = dspy.LM(model=self.model, api_key=self.api_key, temperature=self.temperature)
    else:
      # 使用默认配置
      self.lm = dspy.LM(model=self.model, temperature=self.temperature)
      
    self.dspy.configure(lm=self.lm)
    
  def generate(
    self,
    input_data: Union[str, List[Dict]],
    model: str = None,
    api_key: str = None,
    api_base: str = None,
    model_type: str = None,
    context: str = "",
    # example_relations: Optional[Union[
    #   List[Tuple[str, str, str]],
    #   List[Tuple[Tuple[str, str], str, Tuple[str, str]]]
    # ]] = None,
    chunk_size: Optional[int] = None,
    cluster: bool = False,
    temperature: float = None,
    # node_labels: Optional[List[str]] = None,
    # edge_labels: Optional[List[str]] = None,
    # ontology: Optional[List[Tuple[str, str, str]]] = None,
    output_folder: Optional[str] = None
  ) -> Graph:
    """Generate a knowledge graph from input text or messages.
    
    Args:
        input_data: Text string or list of message dicts
        model: Name of OpenAI model to use
        api_key (str): OpenAI API key for making model calls
        api_base: API base URL for custom endpoints (e.g. SGLang server)
        model_type: Model type (e.g. 'chat' for SGLang)
        chunk_size: Max size of text chunks in characters to process
        context: Description of data context
        example_relations: Example relationship tuples
        node_labels: Valid node label strings
        edge_labels: Valid edge label strings
        ontology: Valid node-edge-node structure tuples
        output_folder: Path to save partial progress
        
    Returns:
        Generated knowledge graph
    """
    
    # Process input data
    is_conversation = isinstance(input_data, list)
    if is_conversation:
      # Extract text from messages
      text_content = []
      for message in input_data:
        if not isinstance(message, dict) or 'role' not in message or 'content' not in message:
          raise ValueError("Messages must be dicts with 'role' and 'content' keys")
        if message['role'] in ['user', 'assistant']:
          text_content.append(f"{message['role']}: {message['content']}")
      
      # Join with newlines to preserve message boundaries
      processed_input = "\n".join(text_content)
    else:
      processed_input = input_data

    if any([model, temperature, api_key, api_base, model_type]):
      # 如果使用 SGLang，则不传递温度参数
      if (api_base or self.api_base) and (model_type or self.model_type):
        self.init_model(
          model=model or self.model,
          api_key=api_key or self.api_key,
          api_base=api_base or self.api_base,
          model_type=model_type or self.model_type
        )
      else:
        self.init_model(
          model=model or self.model,
          temperature=temperature or self.temperature,
          api_key=api_key or self.api_key,
          api_base=api_base or self.api_base,
          model_type=model_type or self.model_type
        )
    
    if not chunk_size:
      entities = get_entities(self.dspy, processed_input, is_conversation=is_conversation)
      relations = get_relations(self.dspy, processed_input, entities, is_conversation=is_conversation)
    else:
      chunks = chunk_text(processed_input, chunk_size)
      entities = set()
      relations = set()

      def process_chunk(chunk):
        chunk_entities = get_entities(self.dspy, chunk, is_conversation=is_conversation)
        chunk_relations = get_relations(self.dspy, chunk, chunk_entities, is_conversation=is_conversation)
        return chunk_entities, chunk_relations

      # Process chunks in parallel using ThreadPoolExecutor
      with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunks))
        
      # Combine results
      for chunk_entities, chunk_relations in results:
        entities.update(chunk_entities)
        relations.update(chunk_relations)
    
    graph = Graph(
      entities = entities,
      relations = relations,
      edges = {relation[1] for relation in relations}
    )
    
    if cluster:
      graph = self.cluster(graph, context)
    
    if output_folder:
      os.makedirs(output_folder, exist_ok=True)
      output_path = os.path.join(output_folder, 'graph.json')
      
      graph_dict = {
        'entities': list(entities),
        'relations': list(relations),
        'edges': list(graph.edges)
      }
      
      with open(output_path, 'w') as f:
        json.dump(graph_dict, f, indent=2)
      
    return graph
    
  def cluster(
    self, 
    graph: Graph,
    context: str = "",
    model: str = None,
    temperature: float = None,
    api_key: str = None,
    api_base: str = None,
    model_type: str = None,
  ) -> Graph:
    # Initialize dspy with new parameters if any are provided
    if any([model, temperature, api_key, api_base, model_type]):
      # 如果使用 SGLang，则不传递温度参数
      if (api_base or self.api_base) and (model_type or self.model_type):
        self.init_model(
          model=model or self.model,
          api_key=api_key or self.api_key,
          api_base=api_base or self.api_base,
          model_type=model_type or self.model_type
        )
      else:
        self.init_model(
          model=model or self.model,
          temperature=temperature or self.temperature,
          api_key=api_key or self.api_key,
          api_base=api_base or self.api_base,
          model_type=model_type or self.model_type
        )

    return cluster_graph(self.dspy, graph, context)
  
  def aggregate(self, graphs: list[Graph]) -> Graph:
    # Initialize empty sets for combined graph
    all_entities = set()
    all_relations = set()
    all_edges = set()
    
    # Combine all graphs
    for graph in graphs:
      all_entities.update(graph.entities)
      all_relations.update(graph.relations)
      all_edges.update(graph.edges)
    
    # Create and return aggregated graph
    return Graph(
      entities=all_entities,
      relations=all_relations,
      edges=all_edges
    )

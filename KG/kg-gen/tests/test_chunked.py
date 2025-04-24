from src.kg_gen import KGGen
import os
from dotenv import load_dotenv

if __name__ == "__main__":
  # Load environment variables
  load_dotenv()
  
  # Example usage
  kg = KGGen()
  
  # Load fresh wiki content
  with open('tests/data/kingkiller_chapter_one.txt', 'r', encoding='utf-8') as f:
  # with open('tests/data/fresh_wiki_article.md', 'r', encoding='utf-8') as f:
    text = f.read()
    
  # # Generate graph from wiki text without chunking
  graph = kg.generate(
    input_data=text,
    model="openai/gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
  )
  print("Without chunking:")
  print("Entities:", graph.entities)
  print("Edges:", graph.edges) 
  print("Relations:", graph.relations)
  
  # Generate graph from wiki text with chunking
  graph_chunked = kg.generate(
    input_data=text,
    model="openai/gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    chunk_size=1000
  )
  print("\nWith chunking:")
  print("Entities:", graph_chunked.entities)
  print("Edges:", graph_chunked.edges)
  print("Relations:", graph_chunked.relations)
  
  # Compare differences
  print("\nDifferences between chunked and non-chunked graph generation:")
  print("Entities found only in chunked graph:", graph_chunked.entities - graph.entities)
  print("Entities found only in non-chunked graph:", graph.entities - graph_chunked.entities)
  print("Edge types found only in chunked graph:", graph_chunked.edges - graph.edges)
  print("Edge types found only in non-chunked graph:", graph.edges - graph_chunked.edges)
  print("Relationships found only in chunked graph:", graph_chunked.relations - graph.relations)
  print("Relationships found only in non-chunked graph:", graph.relations - graph_chunked.relations)

from src.kg_gen import KGGen
import os
from dotenv import load_dotenv

if __name__ == "__main__":
  # Load environment variables
  load_dotenv()
  
  # Example usage
  kg = KGGen()
  
  # Generate a simple graph from conversation
  messages = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."}
  ]
  
  graph = kg.generate(
    input_data=messages,
    model="openai/gpt-4o", 
    api_key=os.getenv("OPENAI_API_KEY")
  )
  print(graph)

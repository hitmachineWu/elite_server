from src.kg_gen import KGGen
import os
from dotenv import load_dotenv

if __name__ == "__main__":
  # Load environment variables
  load_dotenv()
  
  # Example usage
  kg = KGGen()
  
  # Test text input
  text = "Linda is Josh's mother. Ben is Josh's brother. Andrew is Josh's father. Judy is Andrew's sister. Josh is Judy's nephew. Judy is Josh's aunt."
  # Test with different models and their corresponding API keys
  model_configs = [
    {
      "model": "openai/gpt-4o",
      "api_key": os.getenv("OPENAI_API_KEY")
    },
    {
      "model": "anthropic/claude-3-5-sonnet-20240620", 
      "api_key": os.getenv("ANTHROPIC_API_KEY")
    },
    {
      "model": "gemini/gemini-pro",
      "api_key": os.getenv("GEMINI_API_KEY") 
    }
  ]
  
  for config in model_configs:
    print(f"\nTesting with model: {config['model']}")
    try:
      graph = kg.generate(
        input_data=text,
        model=config['model'],
        api_key=config['api_key']
      )
      print(graph)
    except Exception as e:
      print(f"Error with {config['model']}: {str(e)}")

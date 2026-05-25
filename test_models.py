import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize the new client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Fetching available models for your API key...")
print("-" * 30)

try:
    # Just print the exact name of every single model your key can access
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print(f"Error fetching models: {e}")
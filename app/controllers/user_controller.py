# app/controllers/user_controller.py

import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Importing extracted configurations and prompts
from app.config.ai_config import GEMINI_MODEL
from app.prompts.legal_prompts import SYSTEM_PROMPT

# .env file load karne ke liye
load_dotenv()

# Initialize the new Client. It will automatically look for the "GEMINI_API_KEY" in your .env!
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def get_legal_analysis(case_text: str):
    try:
        # Combined prompt execution with system instructions using the NEW SDK
        response = client.models.generate_content(
            model=GEMINI_MODEL, # Using flash as it is highly reliable and fast
            contents=f"System Instructions:\n{SYSTEM_PROMPT}\n\nUser Case Data:\nAnalyze this case: {case_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        # Raw string response from AI
        #  from ai response we need only specific part
        ai_response_string = response.text
        
        # Converting raw string that is coming from AI and it look like json
        #  and we convert it directly into a Python Dictionary so that backend can understand
        return json.loads(ai_response_string)
        
        #  exception handling , if that it take error into e variable and then print it
    except Exception as e:
        print(f"Error executing AI Analysis: {e}")
        #  since this is fn and it is called in router so we have to return something
        #  if error comes so we return none
        return None































        # f"...": Isey Python mein f-string (Formatted String) bolte hain. Iska faida yeh hai ki tum text ke beech mein curly braces {} lagakar kisi bhi variable ko print kara sakte ho
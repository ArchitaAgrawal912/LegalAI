# # app/controllers/user_controller.py

# import os
# import json
# from google import genai
# from dotenv import load_dotenv

# # Importing configurations and updated prompt formatter
# from app.config.ai_config import GEMINI_MODEL, AI_GENERATION_CONFIG, get_gemini_api_key
# from app.prompts.legal_prompts import format_legal_analysis_contents
# from app.core.case_search import fetch_reference_precedents  # <-- 1. Naya search service import kiya

# # .env file load karne ke liye
# load_dotenv()

# # Fetch key securely via our config manager helper
# api_key = get_gemini_api_key()

# # Initialize the new Gemini Client


# client = genai.Client(api_key=api_key)

# async def get_legal_analysis(case_text: str):
#     try:
#         print("\n--------------------------------------------------")
#         print("⚡ CONTROLLER: Starting Legal Analysis Pipeline...")
#         print("--------------------------------------------------")

#         # 2. Indian Kanoon API se live precedents fetch karo
#         reference_cases = await fetch_reference_precedents(case_text)
        
#         # 3. STRICT GUARD: Agar API se koi real case nahi mila, toh yahin se block response bhej do
#         # Isse AI kabhi bhi hallucinated ya fake data nahi bana payega.
#         if not reference_cases:
#             print("🛑 CONTROLLER STOP: Indian Kanoon API returned 0 results. Aborting to prevent hallucination.")
#             return {
#                 "primary_offense": "Analysis Suspended",
#                 "case_summary": "Could not verify reference precedents via Indian Kanoon API.",
#                 "ipc_sections": [],
#                 "bns_sections": [],
#                 "special_and_local_laws": [],
#                 "reference_cases": [],  # Valid empty array matching your updated serializer
#                 "overall_reasoning": "Live legal search returned no corroborating database records. Process stopped to ensure 100% data safety and prevent AI hallucination.",
#                 "overall_severity": "Unknown",
#                 "cognizable": False
#             }
        
#         # 4. Prompt format karke dono parameters pass karo (Text + Real Cases)
#         compiled_contents = format_legal_analysis_contents(case_text, reference_cases)
        
#         print("🧠 CONTROLLER: Sending complete payload to Gemini...")
#         # Combined prompt execution with system instructions using the NEW SDK
#         response = client.models.generate_content(
#             model=GEMINI_MODEL,
#             contents=compiled_contents,
#             config=AI_GENERATION_CONFIG,
#         )
        
#         # Raw string response from AI
#         ai_response_string = response.text
        
#         # Converting raw string directly into a Python Dictionary
#         return json.loads(ai_response_string)
        
#     except Exception as e:
#         print(f"❌ CONTROLLER CRITICAL ERROR: {e}")
#         return None












#  ye file  bas  api kanoon key ko legi and  jo vha se text aaay usey geminni ko degi , taaki reference cases ka pta chal sake 

#  and also take case ka text that advocate fills and reference cases  and a prompt , then it will bring teh ipc and all refernce cases












        # f"...": Isey Python mein f-string (Formatted String) bolte hain. Iska faida yeh hai ki tum text ke beech mein curly braces {} lagakar kisi bhi variable ko print kara sakte ho
# app/core/case_search.py

import httpx
import json
from google import genai
from app.config.ai_config import get_indian_kanoon_api_key, get_gemini_api_key, GEMINI_MODEL

# 🎯 NAYA IMPORT: Tera naya beautify prompt function
from app.prompts.legal_prompts import format_keyword_extraction_prompt, format_beautify_kanoon_prompt

async def fetch_reference_precedents(case_text: str) -> list:
    """
    SMART AI MODE: 
    1. Gemini extracts keywords.
    2. Indian Kanoon fetches raw historical cases.
    3. Gemini beautifies the raw data into clean titles, summaries, and extracted IPCs/BNS.
    """
    
    print("\n--------------------------------------------------")
    print("🧠 STEP 1a: Extracting smart legal keywords using Gemini...")
    
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        print("⚠️ WARNING: Gemini API key missing, returning empty.")
        return []

    try:
        ai_client = genai.Client(api_key=gemini_key)
        prompt_content = format_keyword_extraction_prompt(case_text)
        ai_response = ai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt_content
        )
        clean_query = ai_response.text.strip()
        print(f"🎯 GEMINI EXTRACTED KEYWORDS: '{clean_query}'")
    except Exception as ai_err:
        print(f"❌ Gemini Keyword Extraction Failed: {ai_err}")
        clean_query = " ".join(case_text.split()[:15])

    # ----------------------------------------------------
    # PHASE 2: INDIAN KANOON API CALL (RAW DATA)
    # ----------------------------------------------------
    api_key = get_indian_kanoon_api_key()
    print(f"🚀 STEP 1b: Sending AI Keywords to Indian Kanoon...")
    
    if not api_key:
        return []

    api_key = api_key.replace('"', '').replace("'", "").strip()
    auth_header = f"Token {api_key}" if not api_key.startswith("Token ") else api_key
    url = "https://api.indiankanoon.org/search/"
    headers = {"Authorization": auth_header, "Accept": "application/json"}
    data_payload = {"formInput": clean_query, "pagenum": 0}
    
    raw_cases_for_llm = []

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, data=data_payload)
            if response.status_code == 200:
                docs = response.json().get("docs", [])
                
                # Extract text into a list
                for doc in docs[:3]:
                    title = doc.get("title", "").replace("<b>", "").replace("</b>", "").strip()
                    context = doc.get("context", "").replace("<b>", "").replace("</b>", "").strip()
                    headline = doc.get("headline", "").replace("<b>", "").replace("</b>", "").strip()
                    raw_cases_for_llm.append(f"Case Title: {title} | Snippet: {context} {headline}")
            else:
                return []
    except Exception as e:
        print(f"❌ HTTP CALL FAILED: {e}")
        return []

    if not raw_cases_for_llm:
        return []

    # ----------------------------------------------------
    # PHASE 3: DEDICATED AI BEAUTIFICATION
    # ----------------------------------------------------
    print(f"✨ STEP 1c: Beautifying Kanoon results and extracting laws...")
    
    # 🎯 PROMPT FILE SE DATA AAYA
    beautify_prompt = format_beautify_kanoon_prompt(raw_cases_for_llm)

    try:
        beautify_response = ai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=beautify_prompt
        )
        
        # Clean LLM Output and parse JSON
        clean_json_text = beautify_response.text.strip().replace("```json", "").replace("```", "").strip()
        final_reference_cases = json.loads(clean_json_text)
        return final_reference_cases

    except Exception as e:
        print(f"❌ Gemini Beautification Failed: {e}")
        return [{"title": "Parse Error", "summary": "Failed to parse data", "ipc_bns_applied": "N/A"}]
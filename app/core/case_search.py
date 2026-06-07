# app/core/case_search.py

import json
import httpx
from app.config.ai_config import get_indian_kanoon_api_key
from app.core.ai_service import call_gemini_llm
from app.prompts.legal_prompts import format_keyword_extraction_prompt, format_beautify_kanoon_prompt

async def fetch_reference_precedents(case_text: str) -> list:
    """
    Core Logic Engine:
    1. Extracts smart keywords using Universal AI Service.
    2. Fetches raw historical cases from Indian Kanoon.
    3. Beautifies raw cases into clean JSON matching Pydantic schemas.
    """
    
    # ----------------------------------------------------
    # PHASE 1: KEYWORD EXTRACTION (LLM CALL 1)
    # ----------------------------------------------------
    print("🧠 Service: Extracting smart legal keywords...")
    keyword_prompt = format_keyword_extraction_prompt(case_text)
    
    try:
        clean_query = call_gemini_llm(keyword_prompt)
        print(f"🎯 Keywords: '{clean_query}'")
    except Exception as ai_err:
        print(f"❌ Keyword Extraction Failed: {ai_err}")
        clean_query = " ".join(case_text.split()[:10])

    # ----------------------------------------------------
    # PHASE 2: INDIAN KANOON API CALL (RAW DATA)
    # ----------------------------------------------------
    print("🚀 Service: Hitting Indian Kanoon API...")
    api_key = get_indian_kanoon_api_key()
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
                
                for doc in docs[:3]:
                    title = doc.get("title", "").replace("<b>", "").replace("</b>", "").strip()
                    context = doc.get("context", "").replace("<b>", "").replace("</b>", "").strip()
                    headline = doc.get("headline", "").replace("<b>", "").replace("</b>", "").strip()
                    raw_cases_for_llm.append(f"Case Title: {title} | Snippet: {context} {headline}")
            else:
                print(f"❌ Kanoon API returned status code: {response.status_code}")
                return []
    except Exception as e:
        print(f"❌ Indian Kanoon HTTP Call Failed: {e}")
        return []

    if not raw_cases_for_llm:
        return []

    # ----------------------------------------------------
    # PHASE 3: DEDICATED AI BEAUTIFICATION (LLM CALL 2)
    # ----------------------------------------------------
    print("✨ Service: Beautifying Kanoon results into clean JSON...")
    beautify_prompt = format_beautify_kanoon_prompt(raw_cases_for_llm)

    try:
        clean_json_text = call_gemini_llm(beautify_prompt)
        final_reference_cases = json.loads(clean_json_text)
        return final_reference_cases
    except Exception as e:
        print(f"❌ Gemini Beautification Failed: {e}")
        return []
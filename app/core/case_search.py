import json
import httpx
from app.config.ai_config import get_indian_kanoon_api_key
from app.core.ai_service import call_gemini_llm
from app.prompts.legal_prompts import format_beautify_kanoon_prompt

async def fetch_reference_precedents(sections_query: str) -> list:
    """
    Revised Logic Engine:
    1. Bypasses LLM Keyword extraction (Directly uses Approved Sections).
    2. Fetches raw historical cases from Indian Kanoon using sections.
    3. Beautifies raw cases into clean JSON.
    """
    
    # ----------------------------------------------------
    # PHASE 1: INDIAN KANOON API CALL (Direct Sections Query)
    # ----------------------------------------------------
    print(f"🚀 Service: Fetching Kanoon precedents for: {sections_query}")
    api_key = get_indian_kanoon_api_key()
    if not api_key:
        return []

    api_key = api_key.replace('"', '').replace("'", "").strip()
    auth_header = f"Token {api_key}" if not api_key.startswith("Token ") else api_key
    url = "https://api.indiankanoon.org/search/"
    headers = {"Authorization": auth_header, "Accept": "application/json"}
    
    # 🎯 Direct Section Input as formInput
    data_payload = {"formInput": sections_query, "pagenum": 0}
    
    raw_cases_for_llm = []

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, data=data_payload)
            if response.status_code == 200:
                docs = response.json().get("docs", [])
                
                for doc in docs[:3]: # Sirf top 3 results
                    title = doc.get("title", "").replace("<b>", "").replace("</b>", "").strip()
                    context = doc.get("context", "").replace("<b>", "").replace("</b>", "").strip()
                    raw_cases_for_llm.append(f"Title: {title} | Snippet: {context}")
            else:
                print(f"❌ Kanoon API Error: {response.status_code}")
                return []
    except Exception as e:
        print(f"❌ Indian Kanoon HTTP Call Failed: {e}")
        return []

    if not raw_cases_for_llm:
        return []

    # ----------------------------------------------------
    # PHASE 2: AI BEAUTIFICATION (LLM CALL)
    # ----------------------------------------------------
    print("✨ Service: Beautifying results...")
    beautify_prompt = format_beautify_kanoon_prompt(raw_cases_for_llm)

    try:
        # call_gemini_llm is synchronous, so keep it as is unless it's async
        clean_json_text = call_gemini_llm(beautify_prompt)
        final_reference_cases = json.loads(clean_json_text)
        return final_reference_cases
    except Exception as e:
        print(f"❌ Gemini Beautification Failed: {e}")
        return []
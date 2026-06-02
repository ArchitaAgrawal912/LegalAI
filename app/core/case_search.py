# app/core/case_search.py

import httpx
from google import genai
from app.config.ai_config import get_indian_kanoon_api_key, get_gemini_api_key, GEMINI_MODEL
from app.prompts.legal_prompts import format_keyword_extraction_prompt

async def fetch_reference_precedents(case_text: str) -> list:
    """
    SMART AI MODE: 
    1. Uses Gemini to extract 3-5 solid legal keywords from the full FIR text.
    2. Sends those exact keywords to Indian Kanoon API via POST.
    """
    
    # ----------------------------------------------------
    # PHASE 1: GEMINI SE KEYWORDS EXTRACT KARNA
    # ----------------------------------------------------
    print("\n--------------------------------------------------")
    print("🧠 STEP 1a: Extracting smart legal keywords using Gemini...")
    
    gemini_key = get_gemini_api_key()
    if not gemini_key:
        print("⚠️ WARNING: Gemini API key missing in search service, using fallback splitting.")
        clean_query = " ".join(case_text.split()[:15])  # Fallback agar key na ho
    else:
        try:
            # Initialize Gemini Client
            ai_client = genai.Client(api_key=gemini_key)
            
            # Format prompt for keyword extraction
            prompt_content = format_keyword_extraction_prompt(case_text)
            
            # Call Gemini
            ai_response = ai_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt_content
            )
            
            clean_query = ai_response.text.strip()
            print(f"🎯 GEMINI EXTRACTED KEYWORDS: '{clean_query}'")
            
        except Exception as ai_err:
            print(f"❌ Gemini Keyword Extraction Failed: {ai_err}. Using fallback.")
            clean_query = " ".join(case_text.split()[:15])

    # ----------------------------------------------------
    # PHASE 2: INDIAN KANOON API CALL
    # ----------------------------------------------------
    api_key = get_indian_kanoon_api_key()
    print(f"🚀 STEP 1b: Sending AI Keywords to Indian Kanoon...")
    
    if not api_key:
        print("❌ ERROR: No Indian Kanoon API Key found!")
        return []

    # Token formatting
    api_key = api_key.replace('"', '').replace("'", "").strip()
    auth_header = f"Token {api_key}" if not api_key.startswith("Token ") else api_key

    url = "https://api.indiankanoon.org/search/"
    headers = {
        "Authorization": auth_header,
        "Accept": "application/json"
    }

    # 🔥 Ab data_payload mein hamare smart AI-extracted keywords ja rahe hain!
    data_payload = {
        "formInput": clean_query,
        "pagenum": 0
    }
    
    print(f"📡 Sending POST request to Indian Kanoon with form data: {data_payload}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, data=data_payload)
            
            print(f"📊 LIVE API STATUS CODE RECEIVED: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                docs = data.get("docs", [])
                
                reference_cases = []
                for doc in docs[:3]: # Top 3 cases
                    title = doc.get("title", "Unknown Case")
                    context = doc.get("context", "")
                    headline = doc.get("headline", "")
                    
                    # Clean internal HTML tags
                    clean_title = title.replace("<b>", "").replace("</b>", "").strip()
                    clean_context = context.replace("<b>", "").replace("</b>", "").strip()
                    
                    case_summary = f"Title: {clean_title} | Context: {clean_context} {headline}"
                    reference_cases.append(case_summary)
                    
                return reference_cases
            else:
                print(f"⚠️ Non-200 status code from Indian Kanoon: {response.status_code}")
                return []

    except Exception as e:
        print(f"❌ CRITICAL EXCEPTION DURING HTTP CALL: {e}")
        print("--------------------------------------------------\n")
        return []
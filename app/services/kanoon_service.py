import requests
from app.core.config import INDIAN_KANOON_API_KEY

def get_case_references(query: str) -> list:
    
    url = "https://api.indiankanoon.org/search/"
    
    headers = {
        "Authorization": f"Token {INDIAN_KANOON_API_KEY}"
    }
    
    params = {
        "formInput": query,
        "pagenum": 0
    }
    
    response = requests.post(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return []
    
    data = response.json()
    
    cases = []
    
    for doc in data.get("docs", [])[:5]:
        cases.append({
            "title": doc.get("title", "Unknown"),
            "court": doc.get("docsource", "Unknown"),
            "year": str(doc.get("publishdate", "Unknown")),
            "citation": str(doc.get("tid", ""))
        })
    
    return cases
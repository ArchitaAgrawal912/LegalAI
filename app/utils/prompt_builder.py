def build_legal_prompt(user_query: str):

    return f"""
    You are an Indian legal assistant.

    Analyze the user's legal issue carefully.

    User Query:
    {user_query}

    IMPORTANT:
    - Always provide BOTH IPC and BNS sections wherever applicable.
    - Never leave bns_sections empty if criminal offences are involved.

    Return ONLY valid JSON.

    Format:

    {{
        "ipc_sections": [],
        "bns_sections": [],
        "legal_concepts": [],
        "case_references": [],
        "next_steps": []
    }}

    Do not return markdown.
    Do not return explanation outside JSON.
    """

def build_summary_prompt(case_description: str) -> str:
    return f"""
    You are an Indian Legal Assistant.

    Analyze the following case description and generate:
    1. A concise case title (max 10 words)
    2. A clear case summary(max 100 words, plain language)

    Case Description:
    {case_description}

    Return ONLY valid JSON:
    {{
        "title": "",
        "summary": ""
    }}
    
    Do not return markdown.
    Do not return explanation outside JSON.
    """
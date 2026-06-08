def build_section_prompt(summary: str):

    return f"""
    You are an Indian legal assistant.

    Analyze the user's legal issue carefully.

    Case Summary:
    {summary}

    IMPORTANT:
    - Always provide BOTH IPC and BNS sections wherever applicable.
    - Never leave bns_sections empty if criminal offences are involved.
    - Never give random/ unnessecary ipc_sections or bns_sections

    Return ONLY valid JSON.

    Format:
    {{
        "sections": [
            {{
                "ipc_section": "",
                "bns_section": "",
                "reason": ""
            }}
        ]
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
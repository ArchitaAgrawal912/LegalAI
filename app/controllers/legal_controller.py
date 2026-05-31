import json # Python's built-in library for JSON handling

from groq import Groq  # Groq's official Python SDK — lets you talk to their API

from app.core.config import GROQ_API_KEY
from app.services.kanoon_service import get_case_references
from app.utils.prompt_builder import build_legal_prompt


client = Groq(api_key=GROQ_API_KEY)

# GROQ call

def get_legal_response(user_query: str):

    prompt = build_legal_prompt(user_query)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": "You are a helpful Indian legal assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    final_answer = response.choices[0].message.content.strip()

    final_answer = final_answer.replace("```json", "")
    final_answer = final_answer.replace("```", "")

    parsed_response = json.loads(final_answer)

    # CALL 2 : KANOON
    case_references = get_case_references(user_query)
    

    # Combining both results
    parsed_response["case_references"] = case_references

    return parsed_response

# STORY - MENTAL MODLE >>>

#User sends case description → controller receives it as user_query → prompt builder wraps it into LLM instructions → Groq client sends it to LLaMA server over the internet → LLaMA returns a list of responses → we take the first one → extract the text content → strip extra whitespace → remove markdown symbols → json.loads() converts the JSON string into a Python dictionary → return that dictionary to the route
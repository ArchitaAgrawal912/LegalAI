import json

from groq import Groq

from app.core.config import GROQ_API_KEY
from app.utils.prompt_builder import build_legal_prompt


client = Groq(api_key=GROQ_API_KEY)


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

    return parsed_response
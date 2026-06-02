import json
from groq import Groq
from app.core.config import GROQ_API_KEY
from app.utils.prompt_builder import build_summary_prompt

client = Groq(api_key=GROQ_API_KEY)

def generate_case_summary(case_description: str) -> dict:
    prompt = build_summary_prompt(case_description)

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
    final_answer = final_answer.replace("```json", "").replace("```", "")

    return json.loads(final_answer)

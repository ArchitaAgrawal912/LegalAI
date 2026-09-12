import json
from groq import AsyncGroq

from app.core.config import settings
from app.prompts.similarity_prompt import SIMILARITY_BATCH_PROMPT

client = AsyncGroq(
    api_key=settings.GROQ_API_KEY
)


async def llm_similarity_scores(
    current_case: str,
    precedent_cases: list[str],
) -> list[int]:
    """
    Computes similarity scores for multiple precedents
    in a single LLM call.
    """

    formatted_precedents = ""

    for index, precedent in enumerate(precedent_cases, start=1):
        formatted_precedents += (
            f"Precedent {index}:\n"
            f"{precedent}\n\n"
        )

    prompt = SIMILARITY_BATCH_PROMPT.format(
        current_case=current_case,
        precedent_cases=formatted_precedents,
    )

    try:

        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=100,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Indian Legal Research Assistant. "
                        "Return ONLY a JSON array of integers."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        answer = response.choices[0].message.content.strip()

        print(f"LLM Batch Response : {answer}")

        scores = json.loads(answer)

        if not isinstance(scores, list):
            raise ValueError("Expected JSON array")

        cleaned_scores = [
            max(0, min(int(score), 100))
            for score in scores
        ]

        return cleaned_scores

    except Exception as e:

        print(f"LLM Batch Error : {e}")

        return [50] * len(precedent_cases)
    
#        match = re.search(r"\d+", answer)
#        Ye Python ki regular expression (regex) function hai.
#        Iska matlab:

# \d → koi bhi digit (0-9)
# + → ek ya usse zyada digits

# Matlab

# "Continuous digits dhoondo."
# answer = "Final score is 95 percent."

# Regex ko milega

# 95


# Regex ne pakda

# "82"

# To

# match.group()

# return karega

# "82"


#  return max(0, min(score, 100)) this line help ki agar llm ne 100 se zyada ya 0 se kam score diya toh usko 0 aur 100 ke beech me le aao.
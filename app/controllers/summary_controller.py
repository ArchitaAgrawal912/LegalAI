from app.serializers.llm_serializer import SummaryResponse
from app.utils.llm_helper import call_llm
from app.utils.prompt_builder import build_summary_prompt



def generate_case_summary(case_description: str) -> dict:
    prompt = build_summary_prompt(case_description)


    parsed =  call_llm(
        model="llama-3.3-70b-versatile",

        system_prompt=
        "You are a helpful Indian legal assistant.",

        user_prompt=prompt
    )
    validated = SummaryResponse.model_validate(parsed)

    return validated.model_dump()

 # WHAT IS MODEL_DUMP() ???
 # WHAT WE ARE DOING MODEL_VALIDATE() HERE ???

# dictionary ➡️ model_validate ➡️ Python object ➡️ model_dump ➡️ dictionary
 
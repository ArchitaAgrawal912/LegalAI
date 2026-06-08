import json

from app.serializers.llm_serializer import SectionResponse

from app.utils.llm_helper import call_llm
from app.utils.prompt_builder import build_section_prompt




def generate_sections(summary: str):

    prompt = build_section_prompt(summary)

   

    parsed_response = call_llm(
         model="llama-3.1-8b-instant",

        system_prompt=
        "You are an Indian legal assistant.",

        user_prompt=prompt
    )
    
    validated = SectionResponse.model_validate(parsed_response)

    return validated.model_dump()

    

    # CALL 2 : KANOON
    # case_references = get_case_references(user_query)
    

    # # Combining both results
    # parsed_response["case_references"] = case_references

    # return parsed_response

# STORY - MENTAL MODLE >>>

#User sends case description → controller receives it as user_query → prompt builder wraps it into LLM instructions → Groq client sends it to LLaMA server over the internet → LLaMA returns a list of responses → we take the first one → extract the text content → strip extra whitespace → remove markdown symbols → json.loads() converts the JSON string into a Python dictionary → return that dictionary to the route
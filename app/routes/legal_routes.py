from fastapi import APIRouter, HTTPException

from app.controllers.legal_controller import get_legal_response

from app.serializers.legal_serializer import (
    LegalQueryRequest,
    LegalQueryResponse
)


router = APIRouter(
    prefix="/legal",
    tags=["Legal AI"]
)


@router.post(
    "/legal-query",
    response_model=LegalQueryResponse
)
def legal_query(payload: LegalQueryRequest):

    try:

        llm_response = get_legal_response(payload.query)

        return LegalQueryResponse(
            ipc_sections=llm_response["ipc_sections"],
            bns_sections=llm_response["bns_sections"],
            legal_concepts=llm_response["legal_concepts"],
            case_references=llm_response["case_references"],
            next_steps=llm_response["next_steps"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
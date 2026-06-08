from fastapi import FastAPI
from app.core import logger

from app.routes.legal_routes import router as legal_router

from app.routes.case_routes import router as case_router

from app.routes.section_routes import router as section_router

from app.routes.precedent_routes import router as precedent_router

from app.models.case_model import Case
from app.models.legal_sections import LegalSection
from app.models.user_model import User
from app.models.precedentCase_model import PrecedentCase

app = FastAPI(
    title="Legal AI Assistant"
)


app.include_router(legal_router)
app.include_router(case_router)
app.include_router(section_router)
app.include_router(precedent_router)
from fastapi import FastAPI

from app.routes.legal_routes import router as legal_router

app = FastAPI(
    title="Legal AI Assistant"
)


app.include_router(legal_router)
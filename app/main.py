from fastapi import FastAPI

# 1. Apni saari alag-alag router files yahan import kar
# from app.routes.case_routes import router as case_router
from app.routes.llm_summary import router as summary_router     # Nayi file 1
from app.routes.ipc_bns_generate import router as analysis_router   # Nayi file 2
from app.routes.approve_reject import router as review_router       # Nayi file 3
from app.routes.reference_cases import router as reference_router   # Nayi file 4
from app.routes.delete import router as delete_router               # Nayi file 5
# 👇 Yahan galti se ek space aa gaya tha, ab hata diya hai





from app.core.logging_middleware import LoggingMiddleware

app = FastAPI(
    title="LegalAI Backend API",
    description="Enterprise-grade Legal API",
    version="1.0.0"
)


app.add_middleware(LoggingMiddleware)


# 2. Sabko app (FastAPI) ke saath jod de
# app.include_router(case_router)
app.include_router(summary_router)
app.include_router(analysis_router)
app.include_router(review_router)
app.include_router(reference_router)
app.include_router(delete_router)












@app.get("/", tags=["Home"])
def home():
    return {"message": "LegalAI Server is Running Successfully! 🚀"}
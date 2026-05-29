from fastapi import FastAPI

# 🎯 Saare routes import kar liye
from app.routes.user_routes import router as user_router
from app.routes.case_routes import router as case_router
from app.routes.ipc_routes import router as ipc_router

# FastAPI app initialize ki (Title Swagger UI me dikhega)
app = FastAPI(
    title="LegalAI Backend API",
    description="API for managing Users, Legal Cases, and IPC Sections",
    version="1.0.0"
)

# 🎯 Teeno darwazo (routers) ko app se jod diya
app.include_router(user_router)
app.include_router(case_router)
app.include_router(ipc_router)

# Health Check / Home Route
@app.get("/", tags=["Home"])
def home():
    return {
        "message": "LegalAI Server is Running Successfully! 🚀",
        "docs_url": "Visit http://127.0.0.1:8000/docs to test the APIs."
    }
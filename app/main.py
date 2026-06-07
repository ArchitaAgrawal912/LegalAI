from fastapi import FastAPI, Request
import time

from app.db.database import create_db_and_tables
from app.routes.user_routes import router as user_router
from app.routes.case_routes import router as case_router
from app.routes import ipc_routes
from app.core.logger import logger

import app.models

app = FastAPI()

# =========================================
# MIDDLEWARE - Log every API request
# =========================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"REQUEST | {request.method} {request.url.path}")

    response = await call_next(request)

    duration = round(time.time() - start_time, 3)

    logger.info(f"RESPONSE | {request.method} {request.url.path} | status={response.status_code} | duration={duration}s")

    return response


app.include_router(user_router)
app.include_router(case_router)
app.include_router(ipc_routes.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    logger.info("LegalAI Server Started")


@app.get("/")
def home():
    return {
        "message": "LegalAI Running"
    }
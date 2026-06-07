import time
import logging
from logging.handlers import RotatingFileHandler
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

# 🎯 Logger Setup: 1MB file limit, keeps 3 backups
handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger("api_logger")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    #  when api get hit toh this middle ware me sabse pehel vo diapatch fn me enter karti like llm/summary route entern kia
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # 🎯 Process the request
        
        # call_next bolta hai.

# Iska matlab hai: "Ab tum apna kaam (router/controller/database) kar lo."
        response = await call_next(request)
        
        # 🎯 Check if this is an internal retry (avoid double logging)
        # We check the headers of the incoming request
        if "x-is-retry" not in request.headers:
            process_time = time.time() - start_time
            
            # Simple log message
            log_msg = (
                f"Path: {request.url.path} | "
                f"Method: {request.method} | "
                f"Status: {response.status_code} | "
                f"Duration: {process_time:.4f}s"
            )
            
            # Log based on status code
            if response.status_code >= 400:
                logger.error(log_msg)
            else:
                logger.info(log_msg)

        return response
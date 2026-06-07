import logging
import os
from datetime import datetime

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Log filename with date
log_filename = f"logs/legalai_{datetime.now().strftime('%Y-%m-%d')}.log"

# Suppress noisy loggers FIRST before basicConfig
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# Our custom logger
logger = logging.getLogger("legalai")
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)

# Terminal handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Format
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Attach handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
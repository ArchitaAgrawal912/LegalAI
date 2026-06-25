import os
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the AWS Secret Name (Change this to match your AWS console name)
AWS_SECRET_NAME = os.getenv("AWS_SECRET_NAME", "legalai/backend/env")
AWS_REGION = os.getenv("AWS_REGION_NAME", "ap-southeast-2")

def get_aws_secrets() -> dict:
    """
    Fetches all secrets from AWS Secrets Manager once at startup.
    Falls back quietly to an empty dictionary if running locally without AWS credentials.
    """
    # If we are working locally, we don't want to hang trying to connect to AWS
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=AWS_REGION)
        
        response = client.get_secret_value(SecretId=AWS_SECRET_NAME)
        if 'SecretString' in response:
            print("✅ Successfully fetched configuration from AWS Secrets Manager.")
            return json.loads(response['SecretString'])
            
    except (NoCredentialsError, ClientError) as e:
        print(f"⚠️ AWS Secrets Manager fallback: {e}. Using local environment/.env file...")
    except Exception as e:
        print(f"❌ Unexpected error connecting to AWS Secrets Manager: {e}")
        
    return {}

# 1. Fetch AWS secrets dictionary at initial load
aws_secrets = get_aws_secrets()

# 2. Define our clean Pydantic settings schema
class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Gemini App"
    API_VERSION: str = "v1"
    
    # These fields will read from AWS first, then fallback to .env or system env vars
    GROQ_API_KEY: str = aws_secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    KANOON_API_TOKEN: str = aws_secrets.get("KANOON_API_TOKEN", os.getenv("KANOON_API_TOKEN", ""))
    DATABASE_URL: str = aws_secrets.get("DATABASE_URL", os.getenv("DATABASE_URL", ""))
    
    # If your code needs a generic GEMINI_API_KEY as well:
    GEMINI_API_KEY: str = aws_secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

    # Allows loading from the local .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# 3. Instantiate the settings object globally
settings = Settings()
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

    GROQ_API_KEY: str = aws_secrets.get("GROQ_API_KEY")
    KANOON_API_TOKEN: str = aws_secrets.get("KANOON_API_TOKEN")
    DATABASE_URL: str = aws_secrets.get("DATABASE_URL")
    GEMINI_API_KEY: str = aws_secrets.get("GEMINI_API_KEY")

    # No .env fallback
    model_config = SettingsConfigDict(extra="ignore")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        required_secrets = {
            "GROQ_API_KEY": self.GROQ_API_KEY,
            "KANOON_API_TOKEN": self.KANOON_API_TOKEN,
            "DATABASE_URL": self.DATABASE_URL,
            "GEMINI_API_KEY": self.GEMINI_API_KEY,
        }

        missing = [key for key, value in required_secrets.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required AWS Secrets: {', '.join(missing)}"
            )


# Global settings instance
settings = Settings()
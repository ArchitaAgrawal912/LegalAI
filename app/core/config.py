from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import json
import boto3
from botocore.exceptions import ClientError

class Settings(BaseSettings):
    """
    Strict environment configuration. 
    App will crash on boot if required keys are missing, preventing runtime errors.
    """
    PROJECT_NAME: str = "LegalAI API"
    API_VERSION: str = "v1.0.0"

    # Set defaults to None so Pydantic doesn't crash before AWS is checked
    GROQ_API_KEY: str | None = None
    KANOON_API_TOKEN: str | None = None
    DATABASE_URL: str | None = None
    
    # AWS Configurations
    AWS_SECRET_NAME: str | None = None
    AWS_REGION: str = "eu-north-1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" 
    )

def fetch_aws_secret(secret_name: str, region_name: str) -> dict:
    """Synchronously fetches the secret payload from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']
        try:
            return json.loads(secret_string)
        except json.JSONDecodeError:
            return {"DATABASE_URL": secret_string}
    except ClientError as e:
        raise RuntimeError(f"Failed to fetch secret from AWS: {str(e)}")

@lru_cache
def get_settings() -> Settings:
    """Loads environment variables. Supports dynamic AWS Secrets override."""
    settings = Settings()
    
    # AWS Cloud Override Logic
    if settings.AWS_SECRET_NAME:
        aws_secrets = fetch_aws_secret(settings.AWS_SECRET_NAME, settings.AWS_REGION)
        
        if "DATABASE_URL" in aws_secrets:
            settings.DATABASE_URL = aws_secrets["DATABASE_URL"]
        if "GROQ_API_KEY" in aws_secrets:
            settings.GROQ_API_KEY = aws_secrets["GROQ_API_KEY"]
        if "KANOON_API_TOKEN" in aws_secrets:
            settings.KANOON_API_TOKEN = aws_secrets["KANOON_API_TOKEN"]
        
    # Final safety checks (Crashing here if missing)
    missing_keys = []
    if not settings.DATABASE_URL: missing_keys.append("DATABASE_URL")
    if not settings.GROQ_API_KEY: missing_keys.append("GROQ_API_KEY")
    if not settings.KANOON_API_TOKEN: missing_keys.append("KANOON_API_TOKEN")
    
    if missing_keys:
        raise ValueError(f"CRITICAL: Missing required environment variables: {', '.join(missing_keys)}")
        
    return settings

settings = get_settings()
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Gemini App"
    API_VERSION: str = "v1"
    GROQ_API_KEY: str
    
    # Allows loading from the local .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    mongo_db_name: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    groq_api_key: str
    gemini_api_key: str

    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
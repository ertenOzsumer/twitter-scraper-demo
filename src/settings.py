from pydantic import BaseSettings

class Settings(BaseSettings):
    TWITTER_BEARER_TOKEN: str
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()

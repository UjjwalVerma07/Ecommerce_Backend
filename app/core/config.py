from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    MAIL_HOST: str = Field(..., env="MAIL_HOST")
    MAIL_PORT: int = Field(..., env="MAIL_PORT")
    MAIL_FROM: str = Field(..., env="MAIL_FROM")

    class Config:
        env_file = ".env"
settings = Settings() 
from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import Optional

class Setting(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: Optional[str] = None  

    @model_validator(mode='before')
    def get_database_url(cls, v):
        v['DATABASE_URL'] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v  

    SECRET_KEY: str
    ALGORITM: str

    class Config:
        env_file = '.env'


settings = Setting()
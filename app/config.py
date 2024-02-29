from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings) : 
    env_name : str = "Local" 
    base_url : str = "http://localhost:8000"
    db_url   : str = "postgresql://postgres:abcd@localhost:5432/test_url_shortner"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings : 
    settings = Settings()  
    print(f"Loading Settings for : {settings.env_name}")
    return settings 

from functools import lru_cache
from typing import List, Tuple

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Uvicorn


    # FastAPI settings
    app_name: str = "Call Center Backend API"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

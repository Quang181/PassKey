from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel

from config import get_settings

router = APIRouter()


class StatusEnum(str, Enum):
    OK = "OK"
    FAILURE = "FAILURE"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class HealthCheck(BaseModel):
    title: str = "Call Center Backend Service API"
    status: StatusEnum


@router.get(
    "/health_check",
    response_model=HealthCheck,
    status_code=200,
    tags=["health_check"],
    summary="Health check",
    description="Check if the API is up and running",
)
async def health_check():
    settings = get_settings()
    return HealthCheck(
        title=settings.app_name,
        status=StatusEnum.OK,
    )

import uvicorn
from fastapi import APIRouter, Depends, Request, FastAPI
from .schemas import InfoUserResponse
from src.auth import get_accessor

import jwt
router = APIRouter()

@router.get("")
async def info_user_by_token(info_user = Depends(get_accessor)) -> InfoUserResponse:

    info_convert = InfoUserResponse(**info_user)

    return info_convert

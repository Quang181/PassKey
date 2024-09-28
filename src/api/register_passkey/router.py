from fastapi import APIRouter, Depends, Request, FastAPI
from src.auth import get_accessor
from .dependencies import register_passkey_from_user_service


import jwt
router = APIRouter()

@router.get("")
async def info_user_by_token(info_user = Depends(get_accessor), service = Depends(register_passkey_from_user_service)
                             ):

    register_info = await service.registry_passkey(info_user)
    return register_info



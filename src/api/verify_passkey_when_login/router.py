from fastapi import APIRouter, Depends, Request, FastAPI
from src.auth import get_accessor
from .dependencies import request_verify_passkey_service

router = APIRouter()

@router.get("")
async def verify_passkey_when_login(info_user = Depends(get_accessor),
                             service=Depends(request_verify_passkey_service)):
    register_info = await service.request_verify_passkey(info_user)
    return register_info


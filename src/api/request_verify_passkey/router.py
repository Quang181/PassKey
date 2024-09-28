from fastapi import APIRouter, Depends, Request, FastAPI
from src.auth import get_accessor
from .dependencies import request_verify_passkey_services

router = APIRouter()


@router.get("")
async def verify_passkey_when_login(
        body,
        info_user = Depends(get_accessor),
                             service=Depends(request_verify_passkey_services)):
    status_verify = await service.request_verify_passkey(info_user.get("account_id"), body)
    return status_verify


from fastapi import APIRouter, Depends, Request, FastAPI
from src.auth import get_accessor
from .dependencies import integration_pass_key_use_case
from .schenmas import VerifyRegisterPassKey

router = APIRouter()

@router.post("")
async def info_user_by_token(body: dict, info_user = Depends(get_accessor),
                             service = Depends(integration_pass_key_use_case)) -> VerifyRegisterPassKey:

    register_info = await service.verify_register_passkey(body, info_user)
    data_return = VerifyRegisterPassKey(**register_info)
    return data_return



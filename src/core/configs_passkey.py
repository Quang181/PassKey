from OpenSSL.rand import status

from src.infra.integration_passkey import IntegrationPasskey
from src.auth import get_accessor

from fastapi import APIRouter, Depends, Request, FastAPI
from src.api.login.schemas import LoginSchema, LoginResponseSchema
from src.core.login.ports import LoginUseCase, CreateIfoUser

import jwt
from src.comman import SECRET_KEY
import datetime

# from src.message import
router = APIRouter()

@router.get("")
async def get_config_passkey(info_account:dict = Depends(get_accessor)):
    configs = await IntegrationPasskey(account_id=info_account.get("account_id"), status="delete").list_config_integration()

    data_return = []

    for i in configs:
        data_return.append({
            "id": i.id,
            "username": info_account.get("account_id"),
            "status": i.status,
        })

    return {
        "data" : data_return
    }

from http.client import HTTPException

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

@router.patch("")
async def update_config_passkey(body: dict, info_account:dict = Depends(get_accessor)):
    id_config = body.get("id")
    status = body.get("status")

    configs = await IntegrationPasskey().get_config_by_id(id_config)

    if not id_config:
        raise HTTPException

    if status == configs.status:
        raise HTTPException

    update_config = await IntegrationPasskey().update_status_config(id_config, status)

    if not update_config:
        raise HTTPException

    return {
        "code": 200
    }

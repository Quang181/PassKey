from fastapi import APIRouter, Depends, Request, FastAPI
from src.api.login.schemas import LoginSchema, LoginResponseSchema
from src.core.login.ports import LoginUseCase, CreateIfoUser
from .dependencies import login_service
import jwt
from src.comman import SECRET_KEY
import datetime

# from src.message import
router = APIRouter()


@router.post("")
async def login(
        body: LoginSchema,
        service: LoginUseCase = Depends(login_service)
) -> LoginResponseSchema:
    info_login = CreateIfoUser(**body.__dict__)
    info_account = await service.get_account(info_login)
    info_account["exp"] =datetime.datetime.now() + datetime.timedelta(hours=24)
    token = jwt.encode(info_account, SECRET_KEY, algorithm="HS256")
    data_return = {"token": token,
                    "message": "Login Successful"}

    data_return = LoginResponseSchema(**data_return)
    return data_return

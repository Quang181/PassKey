from fastapi.params import Depends
from src.adapter.login import LoginAdapter
from src.core.login import ports
from src.core.login.services import LoginService


def create_login_repository() -> ports.LoginRepository:
    return LoginAdapter()


def login_service(login_repository: ports.LoginRepository = Depends(create_login_repository)):
    return LoginService(login_repository)
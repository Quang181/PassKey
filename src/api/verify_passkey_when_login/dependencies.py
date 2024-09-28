from fastapi.params import Depends

from src.core.verify_passkey_when_login import ports
from src.adapter.request_verify_when_login import RequestVerifyWhenLoginAdapter
from src.core.verify_passkey_when_login.services import VerifyPassKeyWhenLoginService
from src.infra.connect_redis import Redis

def request_verify_passkey_repository() -> ports.VerifyPasskeyWhenLoginRepository:
    return RequestVerifyWhenLoginAdapter()

def redis_cli():
    return Redis()

def request_verify_passkey_service(integration_passkey= Depends(request_verify_passkey_repository)) \
        -> ports.VerifyPasskeyWhenLoginUseCase:
    return VerifyPassKeyWhenLoginService(integration_passkey, redis_cli())
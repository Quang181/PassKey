from fastapi.params import Depends
from src.adapter.login import LoginAdapter
from src.core.register_passkey import ports
from src.core.register_passkey.services import RegisterPasskeyService
from src.infra.connect_redis import Redis
from src.infra.integration_passkey import IntegrationPasskey


def create_redis_repository():
    return Redis()

def create_info_integration_passkey_repository():
    return IntegrationPasskey()

def register_passkey_from_user_service(redis_cli = Depends(create_redis_repository),
                                       integration_passkey = Depends(create_info_integration_passkey_repository),):
    return RegisterPasskeyService(integration_passkey, redis_cli)
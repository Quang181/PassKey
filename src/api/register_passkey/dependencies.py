from fastapi.params import Depends
from src.adapter.login import LoginAdapter
from src.core.register_passkey import ports
from src.core.register_passkey.services import RegisterPasskeyService
from src.infra.connect_redis import Redis
from src.infra.integration_passkey import IntegrationPasskey
from src.adapter.register_passkey import RegisterPasskeyAdapter
from src.core.register_passkey.ports import IntegrationPassKeyRepository


def create_redis_repository():
    return Redis()

def integration_pass_key() ->IntegrationPassKeyRepository:
    return RegisterPasskeyAdapter()

def register_passkey_from_user_service(redis_cli = Depends(create_redis_repository),
                                       integration_passkey = Depends(integration_pass_key)):
    return RegisterPasskeyService(integration_passkey, redis_cli)
from src.adapter.verify_register_passkey import VerifyRegisterPasskeyAdapter, VerifyRegisterPasskeyRepository
from src.core.verify_register_passkey.services import IntegrationPassKeyService
from fastapi import Depends
from src.adapter.redis_adapter import RedisAdapter
from src.core.verify_register_passkey.ports import VerifyRegisterPasskeyUseCase, VerifyRegisterPasskeyRepository

def integration_pass_key_repository() -> VerifyRegisterPasskeyRepository:
    return VerifyRegisterPasskeyAdapter()

def redis_cli():
    return RedisAdapter().get_connect()

def integration_pass_key_use_case(integration_passkey: VerifyRegisterPasskeyRepository = Depends(integration_pass_key_repository))\
        -> VerifyRegisterPasskeyUseCase:
    return IntegrationPassKeyService(integration_passkey, redis_cli())
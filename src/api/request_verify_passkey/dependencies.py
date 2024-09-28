from src.infra.connect_redis import Redis
from src.core.request_verify_passkey import ports
from src.core.request_verify_passkey.services import RequestVerifyAccount


def request_verify_passkey_services() -> ports.RequestVerifyPassKeyUseCase:
    return RequestVerifyAccount(Redis())
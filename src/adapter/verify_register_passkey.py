from src.core.verify_register_passkey.ports import VerifyRegisterPasskeyRepository
from src.core.verify_register_passkey.schema import InfoRegister
from src.infra.integration_passkey import IntegrationPasskey
from src.message import InternalServerError


class VerifyRegisterPasskeyAdapter(VerifyRegisterPasskeyRepository):
    def __init__(self):
        super().__init__()

    async def create_info_register_passkey(self, info_register: InfoRegister):
        integration_passkey = IntegrationPasskey(**info_register.__dict__)
        status_create = await integration_passkey.create_integration()
        if not status_create:
            raise InternalServerError

    async def check_credential(self, credential_id):
        integration_passkey = IntegrationPasskey(credential_id=credential_id)
        info_credential = await integration_passkey.check_credential()
        return info_credential
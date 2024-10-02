from src.core.verify_passkey_when_login.ports import VerifyPasskeyWhenLoginRepository
from src.infra.integration_passkey import IntegrationPasskey

class RequestVerifyWhenLoginAdapter(VerifyPasskeyWhenLoginRepository):

    def __init__(self):
        super().__init__()

    async def get(self, account_id: str):
        integration_passkey = IntegrationPasskey(account_id=account_id)
        return await integration_passkey.get_integration_by_user()

from src.infra.integration_passkey import IntegrationPasskey
from src.core.register_passkey.ports import IntegrationPassKeyRepository


class RegisterPasskeyAdapter(IntegrationPassKeyRepository):

    def __init__(self):
        super().__init__()

    async def integration_pass_key(self, account_id, status="delete"):
        configs_integration_passkey = IntegrationPasskey(account_id=account_id, status=status)
        return await configs_integration_passkey.list_config_integration()

from .schema import InfoAccount

class IntegrationPassKeyRepository:
    async def integration_pass_key(self, account_id, status):
        raise NotImplementedError()

class RegistryPassKeyUseCase:
    async def registry_passkey(self, info_account: InfoAccount):
        raise NotImplementedError()
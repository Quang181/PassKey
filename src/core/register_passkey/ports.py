from .schema import InfoAccount

class IntegrationPassKey:
    def integration_pass_key(self):
        raise NotImplementedError()

class RegistryPassKeyUseCase:
    def registry_passkey(self, info_account: InfoAccount):
        raise NotImplementedError()
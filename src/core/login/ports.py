from .schema import CreateIfoUser, InfoAccount
class LoginUseCase:
    async def get_account(self, info_account: CreateIfoUser) -> InfoAccount:
        raise NotImplementedError()

class LoginRepository:
     async def get_account(self, info_account: CreateIfoUser):
        raise NotImplementedError()
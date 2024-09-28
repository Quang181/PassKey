from src.infra.account import Account
from src.core.login.ports import LoginRepository
from src.core.login.schema import CreateIfoUser

class LoginAdapter(LoginRepository):
    def __init__(self):
        super().__init__()

    async def get_account(self, info_login: CreateIfoUser):
        info_account = info_login.__dict__

        username = info_account['username']
        password = info_account['password']

        get_info = Account(username=username).get_info_user_by_username()

        return get_info



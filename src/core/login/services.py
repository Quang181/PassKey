from .ports import LoginRepository, LoginUseCase
from .schema import CreateIfoUser
import hashlib
from fastapi import HTTPException
class LoginService(LoginUseCase):

    def __init__(self, repository: LoginRepository):

        self.repository = repository

    async def get_account(self, info_account: CreateIfoUser):
        print("------")
        info_account_db = await self.repository.get_account(info_account)

        if not info_account_db:
            raise HTTPException(status_code=413, detail="Username or Password is incorrect")

        password = info_account.password

        # Băm mật khẩu với SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if hashed_password != info_account_db.password:
            raise HTTPException(status_code=413, detail="Username or Password is incorrect")

        #
        convert_data = {
            "account_id": info_account_db.id,
            "username": info_account_db.username,
            "fullname": info_account_db.fullname,
            "email": info_account_db.email,
        }
        return convert_data


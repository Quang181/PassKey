class VerifyPasskeyWhenLoginRepository:

    def get(self, account_id: str):
        raise NotImplementedError()


class VerifyPasskeyWhenLoginUseCase:
    def request_verify_passkey(self, id_account, ):
        raise NotImplementedError()

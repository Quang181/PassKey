class RequestVerifyPassKeyRepository:

    def get(self):
        raise NotImplementedError()

class RequestVerifyPassKeyUseCase:

    def request_verify_passkey(self, info_account, data_verify):
        raise NotImplementedError()



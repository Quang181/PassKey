
class VerifyRegisterPasskeyRepository:

    def create_info_register_passkey(self, info_register):
        raise NotImplementedError()

    # def check_credential(self, credential_id):
    #     raise NotImplementedError()

class VerifyRegisterPasskeyUseCase:

    def verify_register_passkey(self, data_verify, data_user):
        raise NotImplementedError()


from .ports import VerifyRegisterPasskeyUseCase, VerifyRegisterPasskeyRepository
# from src.message import
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    options_to_json,
    base64url_to_bytes,
)
import uuid
import datetime
from src.comman import rp_id
from fastapi import HTTPException

class IntegrationPassKeyService(VerifyRegisterPasskeyUseCase):

    def __init__(self, integration_passkey: VerifyRegisterPasskeyRepository,
                 redis_cli ):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli

    async def verify_register_passkey(self, data_verify, info_account):
        user_id = info_account.get("user_id")
        username = info_account.get("username")
        fullname = info_account.get("fullname")
        credential_id = data_verify.get("credential_id")

        key_credential = str(user_id) + "###" + "credentials"
        if not credential_id:
            raise HTTPException(status_code=500, detail="No credential")

        check_credential = await self.integration_passkey.check_credential(credential_id)
        if check_credential:
            raise HTTPException(status_code=413, detail="Credential exits")

        credential_request = [i.decode("utf-8") for i in await self.redis_cli.list_value(key_credential)]

        if credential_id not in credential_request and credential_id:
            raise HTTPException(status_code=400, detail="Invalid credential")

        challenge_key = self.redis_cli.get(str(user_id) + str(username) + str(fullname) + "challenge")
        if not challenge_key:
            raise HTTPException(status_code=413, detail="Please request before verify Passkey")

        try:
            registration_verification = verify_registration_response(
                # Demonstrating the ability to handle a plain dict version of the WebAuthn response
                credential={
                    **data_verify
                },
                expected_challenge=challenge_key,
                expected_origin="http://0.0.0.0:8000",
                expected_rp_id=rp_id,
                require_user_verification=True,
            )

            await self.integration_passkey.create_info_register_passkey(self.get_data_create(registration_verification, info_account))

            return {
                "code": 200
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def gen_id_account():
        return str(uuid.uuid4())

    @staticmethod
    def get_time_now():
        return datetime.datetime.now()

    @classmethod
    def get_data_create(cls, info_verify, info_account):
        return {
            "id": cls.gen_id_account(),
            "account_id": info_account.get("account_id"),
            "credential_id": info_verify.credential_id,
            "credential_public_key": info_verify.credential_public_key,
            "sign_count": info_verify.sign_count,
            "aaguid": info_verify.aaguid,
            "fmt": info_verify.fmt,
            "credential_type": info_verify.credential_type if info_verify.credential_type else None,
            "credential_device_type": info_verify.credential_device_type,
            "create_on": cls.get_time_now(),
            "update_one": cls.get_time_now(),
        }

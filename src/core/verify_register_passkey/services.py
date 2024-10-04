from main import configs_passkey
from .ports import VerifyRegisterPasskeyUseCase, VerifyRegisterPasskeyRepository
# from src.message import
# from webauthn import (
#     generate_registration_options,
#     verify_registration_response,
#     options_to_json,
#     base64url_to_bytes,
# )
import webauthn
import uuid
import datetime
from src.comman import rp_id
from fastapi import HTTPException
from src.infra.integration_passkey import IntegrationPasskey
import json
from src.comman import rp, fido_metadata


class IntegrationPassKeyService(VerifyRegisterPasskeyUseCase):

    def __init__(self, integration_passkey: VerifyRegisterPasskeyRepository,
                 redis_cli ):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli

    async def verify_register_passkey(self, data_verify, info_account):
        user_id = info_account.get("account_id")
        response = data_verify.get('response')
        raw_id = data_verify.get("id")

        if not raw_id or not response:
            raise HTTPException(status_code=400, detail="Data in valid")

        if response is None:
            raise

        convert_key = user_id + "challenge"
        challenge_key = await self.redis_cli.get_value_by_key(convert_key)
        if not challenge_key:
            raise HTTPException(status_code=413, detail="Please request before verify Passkey")

        try:
            # registration_verification = verify_registration_response(
            #     # Demonstrating the ability to handle a plain dict version of the WebAuthn response
            #     credential={
            #         **data_verify.get("response")
            #     },
            #     expected_challenge=challenge_key,
            #     expected_origin='http://localhost:8000',
            #     expected_rp_id=rp_id,
            #     require_user_verification=True,
            # )
            auth_data = webauthn.verify_create_webauthn_credentials(
                rp=rp, challenge_b64=challenge_key.decode(), client_data_b64=response["data"],
                attestation_b64=response["attestation"],
                fido_metadata=fido_metadata
            )

            await self.integration_passkey.create_info_register_passkey(self.get_data_create(auth_data, info_account))

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
    def get_data_create(cls, data_verify, info_account):

        return {
            "id": cls.gen_id_account(),
            "account_id": info_account.get("account_id"),
            "sign_count": data_verify.sign_count,
            "aaguid": data_verify.attested_data.aaguid,
            "attestation": data_verify.attestation,
            "public_key_alg": data_verify.public_key_alg,
            "public_key": data_verify.public_key,
            "create_on": cls.get_time_now(),
            "update_one": cls.get_time_now(),
            "status": "active"
        }

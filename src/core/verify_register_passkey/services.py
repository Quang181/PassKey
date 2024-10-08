from main import configs_passkey
from .ports import VerifyRegisterPasskeyUseCase, VerifyRegisterPasskeyRepository
# from src.message import
# from webauthn import (
#     generate_registration_options,
#     verify_registration_response,
#     options_to_json,
#     base64url_to_bytes,
# )
from src import webauthn
import uuid
import datetime
from src.comman import rp_id
from fastapi import HTTPException
from src.infra.integration_passkey import IntegrationPasskey
import json
from src.comman import rp, fido_metadata
import cryptography.x509
import cryptography.exceptions
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.serialization
import cryptography.hazmat.primitives.asymmetric.rsa
import cryptography.hazmat.primitives.asymmetric.padding
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.asymmetric.x25519
import cryptography.hazmat.primitives.asymmetric.x448
import cbor2
import base64


from ...api.register_passkey.dependencies import integration_pass_key


class IntegrationPassKeyService(VerifyRegisterPasskeyUseCase):

    def __init__(self, integration_passkey: VerifyRegisterPasskeyRepository,
                 redis_cli ):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli

    async def verify_register_passkey(self, data_verify, info_account):
        user_id = info_account.get("account_id")
        response = data_verify.get('response')
        cre_id = data_verify.get("id")

        aaguid = self.get_aaguild_by_response(response["attestation"])

        if not cre_id or not response:
            raise HTTPException(status_code=400, detail="Data in valid")

        credential_account = await self.integration_passkey.check_aaguid(str(aaguid), user_id)
        if credential_account:
            raise HTTPException(status_code=400, detail="Credential already exists")

        convert_key = user_id + "challenge"
        challenge_key = await self.redis_cli.get_value_by_key(convert_key)
        if not challenge_key:
            raise HTTPException(status_code=413, detail="Please request before verify Passkey")

        try:
            auth_data = webauthn.verify_create_webauthn_credentials(
                rp=rp, challenge_b64=challenge_key.decode(), client_data_b64=response["data"],
                attestation_b64=response["attestation"],
                fido_metadata=fido_metadata
            )

            await self.integration_passkey.create_info_register_passkey(self.get_data_create(auth_data, info_account, cre_id))

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
    def get_data_create(cls, data_verify, info_account, credential_id):

        return {
            "id": cls.gen_id_account(),
            "cre_id": credential_id,
            "account_id": info_account.get("account_id"),
            "sign_count": data_verify.sign_count,
            "aaguid": data_verify.aaguid,
            "public_key_alg": data_verify.public_key_alg,
            "public_key":  data_verify.public_key.public_bytes(
        cryptography.hazmat.primitives.serialization.Encoding.PEM,
        cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode(),
            "create_on": cls.get_time_now(),
            "update_one": cls.get_time_now(),
            "status": "active"
        }
 #
    @classmethod
    def get_aaguild_by_response(cls, attestation_b64):
        # attestation_b64 = response["attestation"]
        if not attestation_b64:
            raise HTTPException(status_code=413, data_verify="attestation not exits")

        attestation_data = cbor2.loads(base64.b64decode(attestation_b64))
        authenticator_data = webauthn.attestation.AuthenticatorData.from_bytes(attestation_data["authData"])
        return authenticator_data.attested_data.aaguid
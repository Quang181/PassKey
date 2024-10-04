# from http.client import HTTPException
import base64
import os
# from idlelib.configdialog import changes

from fastapi import HTTPException
from .ports import VerifyPasskeyWhenLoginUseCase
# from webauthn.helpers.structs import (
#     PublicKeyCredentialDescriptor,
#     UserVerificationRequirement,
# )
# from webauthn import (
#     generate_authentication_options,
#     verify_authentication_response,
#     options_to_json,
#     base64url_to_bytes,
# )
from src.comman import rp_id, SECRET_KEY
from src.message import InternalServerError
from src.infra.connect_redis import Redis
import json
import jwt
from src import webauthn
from src.comman import rp
import cryptography.x509
import cryptography.exceptions
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.serialization
import cryptography.hazmat.primitives.asymmetric.rsa
import cryptography.hazmat.primitives.asymmetric.padding
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.asymmetric.x25519
import cryptography.hazmat.primitives.asymmetric.x448

class VerifyPassKeyWhenLoginService(VerifyPasskeyWhenLoginUseCase):

    def __init__(self, integration_passkey, redis_cli: Redis):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli

    async def request_verify_passkey(self, info_account):
        try:
            account_id = info_account.get("account_id")
            integrations_passkey = await self.integration_passkey.get(account_id)

            if not integrations_passkey:
                return {
                    "code": 200,
                    "status": "inactive",
                    "data": {}
                }

            public_keys = []
            config_by_public_key = {}

            for i in integrations_passkey:
                cre_id = i.cre_id
                pkey_alg = i.public_key_alg
                sign_counter = i.sign_count
                public_key = i.public_key

                public_keys.append(base64.b64decode(cre_id))
                config_by_public_key[cre_id] = {
                    "pkey_alg": pkey_alg,
                    "sign_counter": sign_counter,
                    "public_key": public_key,
                }

            # public_key = [base64.b64decode(i.public_key) for i in integrations_passkey]


            options, challenge = webauthn.get_webauthn_credentials(
                rp=rp, existing_keys=public_keys, user_verification=webauthn.types.UserVerification.Preferred,
            )


            # for i in integrations_passkey:
            #     credentials = i.credential_id
            #     public_key = i.credential_public_key
            #
            #     credential_ids.append(PublicKeyCredentialDescriptor(id=credentials))
            #     config_public_key.update({
            #         credentials.hex(): public_key.hex()
            #     })

            # challenge = os.urandom(64)
            # challenge_base64 = base64.b64encode(challenge)
            # complex_authentication_options = generate_authentication_options(
            #     rp_id=rp_id,
            #     timeout=12000,
            #     challenge=challenge_base64,
            #     allow_credentials=credential_ids,
            #     user_verification=UserVerificationRequirement.REQUIRED,
            # )


            # challenge = complex_authentication_options.challenge

            if not challenge:
                raise HTTPException(status_code=413, detail="Challenge not create")

            # config_public_key["challenge"] = changes
            #
            key_request_verify_passkey = account_id + "request#verify#passkey"
            self.redis_cli.set_value(key_request_verify_passkey, challenge, 3000)

            if config_by_public_key:
                key_configs_passkey = account_id + "configs##passkey"
                config_by_public_key = json.dumps(config_by_public_key)
                self.redis_cli.set_value(key_configs_passkey, config_by_public_key, 3000)

            return {
                "code": 200,
                "status": "active",
                "data": options
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

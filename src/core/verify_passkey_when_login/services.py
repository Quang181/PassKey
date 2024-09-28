# from http.client import HTTPException
from fastapi import HTTPException
from .ports import VerifyPasskeyWhenLoginUseCase
from webauthn.helpers.structs import (
    PublicKeyCredentialDescriptor,
    UserVerificationRequirement,
)
from webauthn import (
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
    base64url_to_bytes,
)
from src.comman import rp_id, SECRET_KEY
from src.message import InternalServerError
from src.infra.connect_redis import Redis
import json
import jwt

class VerifyPassKeyWhenLoginService(VerifyPasskeyWhenLoginUseCase):

    def __init__(self, integration_passkey, redis_cli: Redis):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli

    async def request_verify_passkey(self, info_account):
        try:
            account_id = info_account.get("account_id")

            integrations_passkey = await self.integration_passkey.get(account_id)
            # temp_token = jwt.encode(info_account, SECRET_KEY, algorithm="HS256")
            #
            # info_account.update({"temp_token": temp_token})

            if not integrations_passkey:
                return {
                    "code": 200,
                    "status": "inactive",
                    "data": {}
                }

            credentials = integrations_passkey.credential_id
            public_key = integrations_passkey.credential_public_key
            key_request_verify_passkey = account_id + "request#verify#passkey"

            complex_authentication_options = generate_authentication_options(
                rp_id=rp_id,
                timeout=12000,
                allow_credentials=[credentials],
                user_verification=UserVerificationRequirement.REQUIRED,
            )

            challenge = complex_authentication_options.challenge
            if not challenge:
                raise HTTPException(status_code=500, detail="Challenge not create")

            data_save_cache = {
                "challenge": challenge,
                "public_key": public_key,
            }

            self.redis_cli.set_value(key_request_verify_passkey, data_save_cache, 300)

            return {
                "code": 200,
                "status": "active",
                "data": json.loads(options_to_json(complex_authentication_options))
            }
        except:
            raise HTTPException(status_code=500, detail="Server error")

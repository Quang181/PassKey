# from http.client import HTTPException
from base64 import urlsafe_b64decode

import cryptography
import jwt
from fastapi import HTTPException
from src.comman import SECRET_KEY
from src.comman import rp_id
from src.infra.connect_redis import Redis
from .ports import RequestVerifyPassKeyUseCase
import json
import cryptography.x509
import cryptography.exceptions
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.serialization
import cryptography.hazmat.primitives.asymmetric.rsa
import cryptography.hazmat.primitives.asymmetric.padding
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.asymmetric.x25519
import cryptography.hazmat.primitives.asymmetric.x448
import os
from src import webauthn
from src.comman import rp
from fastapi import HTTPException
import cryptography.x509
import cryptography.exceptions
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.serialization
import cryptography.hazmat.primitives.asymmetric.rsa
import cryptography.hazmat.primitives.asymmetric.padding
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.asymmetric.x25519
import cryptography.hazmat.primitives.asymmetric.x448

from ...infra.integration_passkey import IntegrationPasskey


class RequestVerifyAccount(RequestVerifyPassKeyUseCase):

    def __init__(self, redis_cli: Redis):
        self.redis_cli = redis_cli

    async def request_verify_passkey(self, account_info, data_verify):
        try:
            account_id = account_info.get('account_id')
            key_configs_passkey = account_id + "configs##passkey"
            key_request_verify_passkey = account_id + "request#verify#passkey"
            response = data_verify.get("response")
            cre_id = response.get("raw_id")
            if not cre_id:
                raise HTTPException(status_code=413, detail="Not credential_id")

            config_passkey = await self.redis_cli.get_value_by_key(key_configs_passkey)
            if not config_passkey:
                raise HTTPException(status_code=413, detail="No configs found")

            challenge = await  self.redis_cli.get_value_by_key(key_request_verify_passkey)
            if not challenge:
                raise HTTPException(status_code=413, detail="No challenge found")

            config_passkey =  json.loads(config_passkey)
            config_public_key = config_passkey.get(cre_id)
            if not config_public_key:
                raise HTTPException(status_code=413, detail="No configs found")

            public_key = config_public_key.get("public_key")
            if not public_key:
                raise HTTPException(status_code=413, detail="No public key found")

            if not config_public_key:
                raise HTTPException(status_code=413, detail="Config passkey not exist")

            pkey_alg = int(config_public_key["pkey_alg"])
            sign_counter = int(config_public_key["sign_counter"])

            pkey = cryptography.hazmat.primitives.serialization.load_pem_public_key(public_key.encode())


            auth_data = webauthn.verify_get_webauthn_credentials(
                challenge_b64=challenge, client_data_b64=response["data"], authenticator_b64=response["authenticator"],
                signature_b64=response["signature"], pubkey=pkey, pubkey_alg=pkey_alg, rp=rp, sign_count=sign_counter
            )


            if not auth_data:
                raise HTTPException(status_code=413, detail="Verification failed")

            sign_counter += 1
            await IntegrationPasskey().update_number_login(account_id, sign_counter, cre_id)

            return {
                "code": 200,
                "message": "Success"
            }

        except Exception as e:
            raise HTTPException(status_code=413, detail="Verification failed")

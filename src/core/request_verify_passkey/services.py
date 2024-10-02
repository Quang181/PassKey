# from http.client import HTTPException
from base64 import urlsafe_b64decode

import jwt
from fastapi import HTTPException
from webauthn import (
    verify_authentication_response,
    base64url_to_bytes,
)

from src.comman import SECRET_KEY
from src.comman import rp_id
from src.infra.connect_redis import Redis
from .ports import RequestVerifyPassKeyUseCase
import json

class RequestVerifyAccount(RequestVerifyPassKeyUseCase):

    def __init__(self, redis_cli: Redis):
        self.redis_cli = redis_cli

    async def request_verify_passkey(self, account_info, data_verify):
        try:
            account_id = account_info.get('account_id')
            convert_key = account_id + "request#verify#passkey"

            config_passkey = await self.redis_cli.get_value_by_key(convert_key)

            if not config_passkey:
                raise HTTPException(status_code=413, detail="No config")

            config_passkey = json.loads(config_passkey)
            challenge = config_passkey.get("challenge")

            credential_id = data_verify.get("rawId")

            if not credential_id:
                raise HTTPException(status_code=413, detail="not access credential")

            credential_id = urlsafe_b64decode(f"{credential_id}===")

            public_key = config_passkey.get(credential_id)
            if not public_key:
                raise HTTPException(status_code=413, detail="Not config public key")

            authentication_verification = verify_authentication_response(
                # Demonstrating the ability to handle a stringified JSON version of the WebAuthn response

                # credential="""{
                #     "id": "ZoIKP1JQvKdrYj1bTUPJ2eTUsbLeFkv-X5xJQNr4k6s",
                #     "rawId": "ZoIKP1JQvKdrYj1bTUPJ2eTUsbLeFkv-X5xJQNr4k6s",
                #     "response": {
                #         "authenticatorData": "SZYN5YgOjGh0NBcPZHZgW4_krrmihjLHmVzzuoMdl2MFAAAAAQ",
                #         "clientDataJSON": "eyJ0eXBlIjoid2ViYXV0aG4uZ2V0IiwiY2hhbGxlbmdlIjoiaVBtQWkxUHAxWEw2b0FncTNQV1p0WlBuWmExekZVRG9HYmFRMF9LdlZHMWxGMnMzUnRfM280dVN6Y2N5MHRtY1RJcFRUVDRCVTFULUk0bWFhdm5kalEiLCJvcmlnaW4iOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJjcm9zc09yaWdpbiI6ZmFsc2V9",
                #         "signature": "iOHKX3erU5_OYP_r_9HLZ-CexCE4bQRrxM8WmuoKTDdhAnZSeTP0sjECjvjfeS8MJzN1ArmvV0H0C3yy_FdRFfcpUPZzdZ7bBcmPh1XPdxRwY747OrIzcTLTFQUPdn1U-izCZtP_78VGw9pCpdMsv4CUzZdJbEcRtQuRS03qUjqDaovoJhOqEBmxJn9Wu8tBi_Qx7A33RbYjlfyLm_EDqimzDZhyietyop6XUcpKarKqVH0M6mMrM5zTjp8xf3W7odFCadXEJg-ERZqFM0-9Uup6kJNLbr6C5J4NDYmSm3HCSA6lp2iEiMPKU8Ii7QZ61kybXLxsX4w4Dm3fOLjmDw",
                #         "userHandle": "T1RWa1l6VXdPRFV0WW1NNVlTMDBOVEkxTFRnd056Z3RabVZpWVdZNFpEVm1ZMk5p"
                #     },
                #     "type": "public-key",
                #     "authenticatorAttachment": "cross-platform",
                #     "clientExtensionResults": {}
                # }""",
                credential={
                    **data_verify
                },
                expected_challenge=base64url_to_bytes(challenge),
                expected_rp_id=rp_id,
                expected_origin="http://localhost:8000",
                credential_public_key=base64url_to_bytes(public_key),
                require_user_verification=True,
            )

            if not authentication_verification:
                return {
                    "status": 413,
                    "message": "verify fail"
                }

            return {
                "status": 200,
                "message": "verify success",
                "token":  jwt.encode(account_info, SECRET_KEY, algorithm="HS256")
            }

        except Exception as e:

            return {
                "status": 413,
                "message": "verify fail"
            }
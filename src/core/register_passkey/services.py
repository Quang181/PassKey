# from
import os
from fastapi import HTTPException
from .ports import RegistryPassKeyUseCase
from .schema import InfoAccount
from src.comman import rp
# from webauthn import (
#     generate_authentication_options,
#     verify_authentication_response,
#     options_to_json,
#     base64url_to_bytes,
# )
# from webauthn.helpers.structs import (
#     AttestationConveyancePreference,
#     AuthenticatorAttachment,
#     AuthenticatorSelectionCriteria,
#     PublicKeyCredentialDescriptor,
#     ResidentKeyRequirement,
# )
# from webauthn import (
#     generate_registration_options,
#     verify_registration_response,
#     options_to_json,
#     base64url_to_bytes,
# )
from src.comman import rp_name, rp_id
import json
from src.infra.connect_redis import Redis
import base64
from src import webauthn

class RegisterPasskeyService(RegistryPassKeyUseCase):

    def __init__(self, integration_passkey, redis_cli: Redis):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli

    async def registry_passkey(self, info_account: InfoAccount):

        user_id = info_account.get("account_id")
        username = info_account.get("username")
        fullname = info_account.get("fullname")

        public_keys = []
        data_save_redis = []
        configs_passkey = await self.integration_passkey.integration_pass_key(account_id=user_id)
        for i in configs_passkey:
            public_keys.append(base64.b64decode(i.public_key))

        user = webauthn.types.User(id=user_id.encode(), display_name=username, name=fullname, icon=None)

        try:
            options, challenge = webauthn.create_webauthn_credentials(
                rp=rp, user=user, existing_keys=public_keys, attachment=None, require_resident=False,
                user_verification=webauthn.types.UserVerification.Discouraged,
                attestation_request=webauthn.types.Attestation.DirectAttestation
            )

            convert_key = user_id + "challenge"
            key_credential = str(user_id) + "###" + "credentials"

            self.redis_cli.set_value(convert_key, challenge, 3000)
            if data_save_redis:
                await self.redis_cli.set_data_list(key_credential, data_save_redis, 3000)

        except webauthn.errors.WebAuthnError as e:
            raise HTTPException(status_code=1001, detail=str(e))


        return {
            "data": options
        }

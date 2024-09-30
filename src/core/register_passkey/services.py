# from
import os

from .ports import RegistryPassKeyUseCase
from .schema import InfoAccount
from webauthn import (
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
    base64url_to_bytes,
)
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    ResidentKeyRequirement,
)
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    options_to_json,
    base64url_to_bytes,
)
from src.comman import rp_name, rp_id
import json
from src.infra.connect_redis import Redis
import base64


class RegisterPasskeyService(RegistryPassKeyUseCase):

    def __init__(self, integration_passkey, redis_cli: Redis):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli

    async def registry_passkey(self, info_account: InfoAccount):

        user_id = info_account.get("account_id")
        username = info_account.get("username")
        fullname = info_account.get("fullname")

        credential_ids = []
        data_save_redis = []
        configs_passkey = await self.integration_passkey.integration_pass_key(account_id=user_id)
        for i in configs_passkey:
            credential_id = i.credential_id
            credential_ids.append(PublicKeyCredentialDescriptor(id=credential_id.encode("utf-8")))
            data_save_redis.append(credential_id)

        challenge = os.urandom(64)
        challenge_base64 = base64.b64encode(challenge)

        complex_registration_options = generate_registration_options(
            rp_id=rp_id,
            rp_name=rp_name,
            user_id=user_id.encode('utf-8'),
            user_name=username,
            user_display_name=fullname,
            challenge=challenge_base64,
            exclude_credentials=credential_ids,
            attestation=AttestationConveyancePreference.DIRECT,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                resident_key=ResidentKeyRequirement.PREFERRED,
            ), )

        convert_key = str(user_id) + str(username) + str(fullname) + "challenge"
        key_credential = str(user_id) + "###" + "credentials"

        self.redis_cli.set_value(convert_key, challenge_base64, 300)
        if data_save_redis:
            await self.redis_cli.set_data_list(key_credential, data_save_redis, 300)

        return {
            "data": json.loads(options_to_json(complex_registration_options))
        }

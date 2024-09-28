# from
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

class RegisterPasskeyService(RegistryPassKeyUseCase):

    def __init__(self, integration_passkey, redis_cli: Redis):
        self.integration_passkey = integration_passkey
        self.redis_cli = redis_cli


    async def registry_passkey(self, info_account: InfoAccount):

        user_id = info_account.get("account_id")
        username = info_account.get("username")
        fullname = info_account.get("fullname")

        complex_registration_options = generate_registration_options(
            rp_id=rp_id,
            rp_name=rp_name,
            user_id=user_id.encode('utf-8'),
            user_name=username,
            user_display_name=fullname,
            attestation=AttestationConveyancePreference.DIRECT,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                resident_key=ResidentKeyRequirement.PREFERRED,
            ),)

        convert_key = str(user_id) + str(username) + str(fullname) + "challenge"
        self.redis_cli.set_value(convert_key, complex_registration_options.challenge, 300)

        return {
            "data": json.loads(options_to_json(complex_registration_options))
        }




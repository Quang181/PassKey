import base64

import webauthn
import json
import os

class User:
    def __init__(self, user_id: str, display_name: str, name: str, icon=None):
        self.id = self.convert_type_user_id(user_id)
        self.display_name = display_name
        self.name = name
        self.icon = icon

    @staticmethod
    def convert_type_user_id(user_id) -> str:
        if isinstance(user_id, str):
            user_id = bytes(user_id, encoding='utf-8')

        return user_id


class WebAuthn:

    def __init__(self, user: object):
        self.rp = self.creat_relying_party()
        self.user = self.create_credential_user(user)

    @staticmethod
    def creat_relying_party():
        rp = webauthn.types.RelyingParty(
            id="as207960-webauthn.eu.ngrok.io",
            name="AS207960",
            icon="https://as207960.net/assets/img/logo.svg"
        )
        return rp

    def create_credential_user(self, user: object):
        if isinstance(user, User):
            user = webauthn.types.User(**user.__dict__)

        return user

    @staticmethod
    def create_fido_metadata():
        return webauthn.metadata.get_metadata()


    def create_webauthn_credentials(self):
        user = webauthn.types.User(
            id=b"test",
            display_name="Test user",
            name="test@example.com",
            icon=None
        )

        rp = webauthn.types.RelyingParty(
            id="as207960-webauthn.eu.ngrok.io",
            name="AS207960",
            icon="https://as207960.net/assets/img/logo.svg"
        )
        data, challenge = webauthn.create_webauthn_credentials(
            rp=rp, user=user, existing_keys=[],
            attachment=None, require_resident=False,
            user_verification=webauthn.types.UserVerification.Preferred,
            attestation_request=webauthn.types.Attestation.DirectAttestation,
        )

        return data, challenge


    def verify_create_webauthn_credentials(self, response, challenge):
        auth_data = webauthn.verify_create_webauthn_credentials(
            rp=self.rp,
            challenge_b64=challenge,
            client_data_b64=response["data"],
            attestation_b64=response["attestation"],
            fido_metadata= self.create_fido_metadata()
        )

        return auth_data

    def generate_request_verify_passkey(self, public_keys: list):
        options, challenge = webauthn.get_webauthn_credentials(
            rp= self.rp,
            existing_keys= public_keys,
            user_verification=webauthn.types.UserVerification.Preferred,
        )

        return options, challenge

    def verify_response_passkey(self, response, challenge):
        auth_data = webauthn.verify_create_webauthn_credentials(
            rp=self.rp, challenge_b64=challenge,
            client_data_b64=response["data"],
            attestation_b64=response["attestation"],
            fido_metadata= None
        )

        return auth_data

if __name__ == '__main__':

    user = User("1ejhwqeqweqeq", "quang", "Minh")

    web_authn = WebAuthn(user)

    c, b = web_authn.create_webauthn_credentials()
    print(c)
    print(b)

    # Giả lập dữ liệu clientDataJSON
    client_data = {
        "type": "webauthn.get",
        "challenge": b,
        "origin": "https://example.com",
        "crossOrigin": False
    }
    client_data_json = json.dumps(client_data).encode('utf-8')
    client_data_b64 = base64.urlsafe_b64encode(client_data_json).decode('utf-8')

    # Giả lập attestationObject
    attestation_object = {
        "fmt": "none",
        "authData": base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')  # Dữ liệu ngẫu nhiên giả
    }
    attestation_b64 = base64.urlsafe_b64encode(json.dumps(attestation_object).encode('utf-8')).decode('utf-8')

    fake_response = {
        "data": client_data_b64,
        "attestation": attestation_b64
    }

    web_authn.verify_create_webauthn_credentials(fake_response, b)
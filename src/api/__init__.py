from .login.router import router as login
from .info_user_by_token.router import router as info_user_by_token
from .register_passkey.router import router as register_passkey
from .verify_register_passkey.router import router as verify_register_passkey
from .verify_passkey_when_login.router import router as verify_passkey_when_login
from .request_verify_passkey.router import router as request_verify_passkey

__all__ = ["login", "info_user_by_token", "register_passkey", "verify_register_passkey", "verify_passkey_when_login",
           "request_verify_passkey"]

from fastapi import FastAPI
from WebAuthn import WebAuthn
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# from src.router import
from src.api import (login, verify_register_passkey, verify_passkey_when_login, request_verify_passkey, info_user_by_token, \
    register_passkey)
app = FastAPI()


@app.get("/")
async def root():
    return {"message.py": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message.py": f"Hello {name}"}


def register_routes(app: FastAPI) -> FastAPI:
    # app.include_router(root.router)
    app.include_router(login, prefix="/login", tags=["PassKey"])
    app.include_router(verify_register_passkey, prefix="/verify/register-passkey", tags=["PassKey"])
    app.include_router(verify_passkey_when_login, prefix="/verify/passkey", tags=["PassKey"])
    app.include_router(request_verify_passkey, prefix="/request/verify-passkey", tags=["PassKey"])
    app.include_router(info_user_by_token, prefix="/account/token", tags=["PassKey"])
    app.include_router(register_passkey, prefix="/register/passkey", tags=["PassKey"])

    return app


app = FastAPI()

# Cấu hình CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    app = register_routes(app)
    uvicorn.run(app, host='0.0.0.0', port=8000)
from fastapi import FastAPI
from WebAuthn import WebAuthn
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# from src.router import
from src.api import (login, verify_register_passkey, verify_passkey_when_login, request_verify_passkey, info_user_by_token, \
    register_passkey)

from src.api.template.home import router as home_page
app = FastAPI()


@app.get("/")
async def root():
    return {"message.py": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message.py": f"Hello {name}"}


@app.get("/configs-passkey")
async def configs_passkey():
    return {
        "data": [
            {
                "id_passkey": "123456789",
                "username": "test1",
                "status": "active"
            },
            {
                "id_passkey": "0987654321",
                "username": "test2",
                "status": "active"
            },
            {
                "id_passkey": "09876543222",
                "username": "test3",
                "status": "deactive"
            }
        ]
    }

@app.patch("/configs-passkey")
async def configs_passkey(body: dict):
    return {
        "data": {
            "code": 200,
            "message": "success"
        }
    }

def register_routes(app: FastAPI) -> FastAPI:
    # app.include_router(root.router)
    app.include_router(login, prefix="/login", tags=["PassKey"])
    app.include_router(verify_register_passkey, prefix="/verify/register-passkey", tags=["PassKey"])
    app.include_router(request_verify_passkey, prefix="/verify/passkey", tags=["PassKey"])
    app.include_router(verify_passkey_when_login, prefix="/request/verify-passkey", tags=["PassKey"])
    app.include_router(info_user_by_token, prefix="/account/token", tags=["PassKey"])
    app.include_router(register_passkey, prefix="/register/passkey", tags=["PassKey"])
    app.include_router(home_page, prefix="/home", tags=["HomePage"])
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
# app.config['ENABLE_WEBAUTHN'] = False




if __name__ == '__main__':
    app = register_routes(app)
    uvicorn.run(app, host='0.0.0.0', port=8000)
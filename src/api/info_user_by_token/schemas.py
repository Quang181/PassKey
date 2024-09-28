from fastapi.openapi.models import Schema
from pydantic import BaseModel

class InfoUserResponse(BaseModel):
    type_token: str
    username: str
    password: str
    id: str
    fullname: str
    email: str

class TokenSchema(BaseModel):
    token: str
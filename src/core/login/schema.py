from typing import Optional

from pydantic import BaseModel, Field

class CreateIfoUser(BaseModel):
    username: str
    password: str


class InfoAccount(BaseModel):
    username: str
    password: str
    id: str
    fullname: str
    email: str
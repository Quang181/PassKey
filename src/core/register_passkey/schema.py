from pydantic import BaseModel, Field

class InfoAccount(BaseModel):
    username: str
    password: str
    id: str
    fullname: str
    email: str
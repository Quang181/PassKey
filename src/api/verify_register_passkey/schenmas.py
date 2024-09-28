from pydantic import BaseModel

class VerifyRegisterPassKey(BaseModel):
    code: int

from datetime import datetime

from pydantic import BaseModel, Field

class InfoRegister(BaseModel):
    id: str
    account_id: str
    credential_id: str
    credential_public_key: str
    sign_count: int
    aaguid: str
    fmt: str
    credential_type: str
    credential_device_type: str
    create_on: datetime
    update_one: datetime

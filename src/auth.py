from starlette.requests import Request
from src.message import SessionUnauthorized
import jwt
from src.comman import SECRET_KEY
from fastapi import HTTPException

async def get_accessor(request: Request):
    try:

        headers = request.headers
        authorization = headers.get('Authorization')
        if authorization:
            token = authorization.split('Bearer ')[-1]
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return dict(
                **data
            )
        else:
            raise SessionUnauthorized

    except Exception as e:
        print(e)
    raise HTTPException(status_code=401, detail="SESSION_UNAUTHORIZED")

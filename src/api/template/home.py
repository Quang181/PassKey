
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

templates = Jinja2Templates(directory="src")
router = APIRouter()

@router.get("")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="test.html", context={}
    )

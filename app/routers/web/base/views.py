from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core import config

router = APIRouter()
templates = Jinja2Templates(
    directory=config.BASE_DIR / "templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def index(
        request: Request,
):
    context = {
        "request": request,
    }
    return templates.TemplateResponse('index.html', context)

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import PositiveInt

from core import config
from repositories.user import UsersCRUD
from routers.web.user.dependencies import get_users_crud

router = APIRouter(
    prefix="/users",
)
templates = Jinja2Templates(
    directory=config.BASE_DIR / "templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def get_user_list(
    request: Request,
    crud: UsersCRUD = Depends(get_users_crud),
):
    users = await crud.get_all()
    context = {
        "request": request,
        "users": users,
    }
    return templates.TemplateResponse('users.html', context)


@router.get(
    "/{user_id}",
    response_class=HTMLResponse
)
async def get_user_by_id(
    request: Request,
    user_id: PositiveInt,
    crud: UsersCRUD = Depends(get_users_crud),
):
    user = await crud.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User #{user_id} not found",
        )

    context = {
        "request": request,
        "user": user,
    }
    return templates.TemplateResponse('user.html', context)

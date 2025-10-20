from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import PositiveInt

from core import config
from repositories.post import PostsCRUD
from routers.web.post.dependencies import get_posts_crud

router = APIRouter(
    prefix="/posts",
)
templates = Jinja2Templates(
    directory=config.BASE_DIR / "templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def get_post_list(
    request: Request,
    crud: PostsCRUD = Depends(get_posts_crud),
):
    posts = await crud.get_all()
    context = {
        "request": request,
        "posts": posts,
    }
    return templates.TemplateResponse('posts.html', context)


@router.get(
    "/{post_id}",
    response_class=HTMLResponse
)
async def get_post_by_id(
    request: Request,
    post_id: PositiveInt,
    crud: PostsCRUD = Depends(get_posts_crud),
):
    print('Поиск поста')
    post = await crud.get_with_user_by_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post #{post_id} not found",
        )

    context = {
        "request": request,
        "post": post,
    }
    return templates.TemplateResponse('post.html', context)

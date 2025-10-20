from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt

from repositories.post import PostsCRUD
from routers.api.post.dependencies import get_posts_crud
from schemas import post as schemas

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get(
    "/",
    response_model=list[schemas.PostReadSchema]
)
async def get_posts_list(
    crud: PostsCRUD = Depends(get_posts_crud)
) -> list[schemas.PostReadSchema]:
    return await crud.get_all()



@router.get(
    "/{post_id}/",
    response_model=schemas.PostReadSchema,
)
async def get_post_by_id(
    post_id: PositiveInt,
    crud: PostsCRUD = Depends(get_posts_crud)
) -> schemas.PostReadSchema:
    post = await crud.get_by_id(post_id)
    if post:
        return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post #{post_id} not found",
    )


@router.post(
    "/",
    response_model=schemas.PostReadSchema,
    status_code=201
)
async def create_post(
    new_user: schemas.PostCreateSchema,
    crud: PostsCRUD = Depends(get_posts_crud),
):
    return await crud.create(new_user)

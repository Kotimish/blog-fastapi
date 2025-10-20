from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt

from repositories.user import UsersCRUD
from routers.api.user.dependencies import get_users_crud
from schemas import user as schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/",
    response_model=list[schemas.UserReadSchema]
)
async def get_user_list(
    crud: UsersCRUD = Depends(get_users_crud),
) -> list[schemas.UserReadSchema]:
    return await crud.get_all()


@router.get(
    "/{user_id}/",
    response_model=schemas.UserReadSchema,
)
async def get_user_by_id(
    user_id: PositiveInt,
    crud: UsersCRUD = Depends(get_users_crud),
) -> schemas.UserReadSchema:
    user = await crud.get_by_id(user_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User #{user_id} not found",
    )

@router.post(
    "/",
    response_model=schemas.UserReadSchema,
    status_code=201
)
async def create_user(
    new_user: schemas.UserCreateSchema,
    crud: UsersCRUD = Depends(get_users_crud),
):
    return await crud.create(new_user)

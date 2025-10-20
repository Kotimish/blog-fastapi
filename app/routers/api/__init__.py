from fastapi import APIRouter

from routers.api.post.views import router as post_router
from routers.api.user.views import router as user_router

router = APIRouter(
    prefix='/api',
    tags=['api'],
)

router.include_router(user_router)
router.include_router(post_router)

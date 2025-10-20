from fastapi import APIRouter

from routers.web.base.views import router as base_router
from routers.web.post.views import router as post_router
from routers.web.user.views import router as user_router

router = APIRouter()

router.include_router(base_router)
router.include_router(user_router)
router.include_router(post_router)

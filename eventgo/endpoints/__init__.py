from fastapi import APIRouter

from eventgo.endpoints.auth import router as auth_router
from eventgo.endpoints.user import router as user_router
from eventgo.endpoints.event import router as event_router
from eventgo.endpoints.admin import router as admin_router
from eventgo.endpoints.order import router as order_router

routers = APIRouter()

api_routers = APIRouter(prefix="/api")
api_routers.include_router(auth_router, tags=["Auth"])
api_routers.include_router(user_router, tags=["User"])
api_routers.include_router(event_router, tags=["Event"])
api_routers.include_router(admin_router, tags=["Admin"])
api_routers.include_router(order_router, tags=["Order"])

routers.include_router(api_routers)
from fastapi import APIRouter

from eventgo.endpoints.auth import router as auth_router
from eventgo.endpoints.user import router as user_router
from eventgo.endpoints.event import router as event_router

routers = APIRouter()

api_routers = APIRouter(prefix="/api")
api_routers.include_router(auth_router, tags=["Auth"])
api_routers.include_router(user_router, tags=["User"])
api_routers.include_router(event_router, tags=["Event"])

routers.include_router(api_routers)
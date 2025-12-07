import logging
from typing import Annotated

from fastapi import Depends, Path, Request, WebSocket, WebSocketException, status

from eventgo.config import config
from eventgo.db.schemas.user import UserSchema
from eventgo.db.session import session_manager
from eventgo.services.auth import AuthService
from eventgo.utils.enums import TokenType
from eventgo.utils.exceptions import UnauthorizedError


async def get_session():
    async with session_manager.session() as session:
        yield session


async def check_auth(request: Request, session=Depends(get_session)) -> UserSchema:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise UnauthorizedError("token not provided")
    return await AuthService(session).validate_token(access_token, TokenType.access)


async def check_admin(user: UserSchema = Depends(check_auth)) -> UserSchema:
    if not user.is_superuser:
        raise UnauthorizedError("admin access required")
    return user


async def res_check_auth(
    request: Request, session=Depends(get_session)
) -> UserSchema | None:
    try:
        return await check_auth(request, session)
    except:
        return None


OAuth = Annotated[UserSchema, Depends(check_auth)]
AdminOAuth = Annotated[UserSchema, Depends(check_admin)]
UnstrictedOAuth = Annotated[UserSchema | None, Depends(res_check_auth)]
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    first_name: str
    second_name: str
    third_name: str | None = None
    email: EmailStr
    is_superuser: bool = False


class UserSchema(UserBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    third_name: str | None = None
    email: EmailStr | None = None
    is_superuser: bool | None = None
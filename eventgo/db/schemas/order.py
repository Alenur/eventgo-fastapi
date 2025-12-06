from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from eventgo.utils.enums import OrderStatusType


class OrderBaseSchema(BaseModel):
    user_id: UUID
    status: OrderStatusType


class OrderSchema(OrderBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class OrderCreateSchema(OrderBaseSchema):
    pass


class OrderUpdateSchema(BaseModel):
    status: OrderStatusType | None = None

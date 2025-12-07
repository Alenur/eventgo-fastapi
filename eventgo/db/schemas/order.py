from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, computed_field

from eventgo.db.schemas.order_item import OrderItemDetailSchema, OrderItemInputSchema
from eventgo.utils.enums import OrderStatusType


class OrderBaseSchema(BaseModel):
    user_id: UUID
    status: OrderStatusType


class OrderSchema(OrderBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class OrderCreateSchema(BaseModel):
    status: OrderStatusType
    items: list[OrderItemInputSchema]


class OrderUpdateSchema(BaseModel):
    status: OrderStatusType | None = None


class OrderDetailSchema(BaseModel):
    order_id: UUID
    status: OrderStatusType
    user_id: UUID
    created_at: datetime
    items: list[OrderItemDetailSchema]
    
    @computed_field
    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrderItemBaseSchema(BaseModel):
    order_id: UUID
    available_ticket_id: UUID
    quantity: int
    final_price: float


class OrderItemSchema(OrderItemBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class OrderItemCreateSchema(OrderItemBaseSchema):
    pass


class OrderItemUpdateSchema(BaseModel):
    available_ticket_id: UUID | None = None
    quantity: int | None = None
    final_price: float | None = None

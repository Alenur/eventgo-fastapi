from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, computed_field

from eventgo.utils.enums import TicketType


class OrderItemBaseSchema(BaseModel):
    order_id: UUID
    ticket_id: UUID


class OrderItemSchema(OrderItemBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class OrderItemCreateSchema(OrderItemBaseSchema):
    pass


class OrderItemInputSchema(BaseModel):
    ticket_id: UUID
    quantity: int


class OrderItemUpdateSchema(BaseModel):
    ticket_id: UUID | None = None


class OrderItemDetailSchema(BaseModel):
    ticket_id: UUID
    name: TicketType
    price: float
    quantity: int
    
    @computed_field
    @property
    def total(self) -> float:
        return self.price * self.quantity

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from eventgo.utils.enums import TicketType


class TicketBaseSchema(BaseModel):
    event_id: UUID
    type: TicketType
    price: float
    total_count: int
    available_count: int


class TicketSchema(TicketBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class TicketCreateSchema(BaseModel):
    type: TicketType
    price: float
    total_count: int
    available_count: int


class TicketUpdateSchema(BaseModel):
    type: TicketType | None = None
    price: float | None = None
    total_count: int | None = None
    available_count: int | None = None

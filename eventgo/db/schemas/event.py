from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from eventgo.utils.enums import EventCategory


class EventBaseSchema(BaseModel):
    title: str
    description: str | None = None
    category: EventCategory
    address: str
    start_time: datetime
    end_time: datetime
    image_url: str | None = None


class EventSchema(EventBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


class EventCreateSchema(EventBaseSchema):
    pass


class EventUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    category: EventCategory | None = None
    address: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    image_url: str | None = None
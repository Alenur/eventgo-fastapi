import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status, Query

from eventgo.db.schemas.event import EventCreateSchema, EventSchema, EventUpdateSchema
from eventgo.db.schemas.available_ticket import AvailableTicketSchema
from eventgo.endpoints.dependencies import OAuth, get_session
from eventgo.services.event import EventService

router = APIRouter(prefix="/events")

logger = logging.getLogger(__name__)


@router.get("/", response_model=list[EventSchema], status_code=status.HTTP_200_OK)
async def get_events(
    session=Depends(get_session),
    start: str = Query(..., description="Starting index or 'last' for the latest events"),
    count: int = Query(..., ge=1, le=50, description="Number of events to retrieve")
):
    event_service = EventService(session)
    return await event_service.get_paginated_events(start, count)


@router.get("/{id}", response_model=EventSchema, status_code=status.HTTP_200_OK)
async def get_event_by_id(
    id: UUID,
    session=Depends(get_session)
):
    event_service = EventService(session)
    return await event_service.get_event_by_id(id)


@router.get(
    "/{id}/tickets", response_model=list[AvailableTicketSchema], status_code=status.HTTP_200_OK
)
async def get_event_tickets(
    id: UUID,
    session=Depends(get_session)
):
    event_service = EventService(session)
    return await event_service.get_event_tickets(id)
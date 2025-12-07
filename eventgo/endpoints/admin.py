import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status, Query

from eventgo.db.schemas.event import EventCreateSchema, EventSchema, EventUpdateSchema
from eventgo.db.schemas.ticket import TicketSchema, TicketCreateSchema, TicketUpdateSchema
from eventgo.endpoints.dependencies import AdminOAuth, get_session
from eventgo.services.event import EventService
from eventgo.services.ticket import TicketService

router = APIRouter(prefix="/admin")

logger = logging.getLogger(__name__)


@router.post("/events", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreateSchema,
    admin: AdminOAuth,
    session=Depends(get_session),
):
    event_service = EventService(session)
    return await event_service.create_event(event)


@router.patch("/events/{id}", response_model=EventSchema, status_code=status.HTTP_200_OK)
async def update_event(
    id: UUID,
    data: EventUpdateSchema,
    admin: AdminOAuth,
    session=Depends(get_session),
):
    event_service = EventService(session)
    return await event_service.update_event_by_id(id, data)


@router.delete("/events/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    id: UUID,
    admin: AdminOAuth,
    session=Depends(get_session),
):
    event_service = EventService(session)
    await event_service.delete_event_by_id(id)


@router.post("/events/{id}/tickets", response_model=TicketSchema, status_code=status.HTTP_200_OK)
async def create_event_ticket(
    id: UUID,
    ticket: TicketCreateSchema,
    admin: AdminOAuth,
    session=Depends(get_session),
):
    ticket_service = TicketService(session)
    return await ticket_service.create_ticket(ticket, id)


@router.patch("/tickets/{id}", response_model=TicketSchema, status_code=status.HTTP_200_OK)
async def update_event_ticket(
    id: UUID,
    data: TicketUpdateSchema,
    admin: AdminOAuth,
    session=Depends(get_session),
):
    ticket_service = TicketService(session)
    return await ticket_service.update_ticket_by_id(id, data)


@router.delete("/tickets/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_ticket(
    id: UUID,
    admin: AdminOAuth,
    session=Depends(get_session),
):
    ticket_service = TicketService(session)
    await ticket_service.delete_ticket_by_id(id)
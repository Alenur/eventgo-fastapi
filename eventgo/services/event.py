from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.schemas.event import EventCreateSchema, EventSchema, EventUpdateSchema
from eventgo.db.schemas.ticket import TicketSchema
from eventgo.services.ticket import TicketService
from eventgo.repositories.event import EventRepository
from eventgo.utils.exceptions import NotFoundError


class EventService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = EventRepository(session)

    async def get_event_by_id(self, event_id: UUID) -> EventSchema:
        event = await self._repository.get_by_id(event_id)
        if event is None:
            raise NotFoundError(f"event_id: {event_id}")
        return EventSchema.model_validate(event, from_attributes=True)

    async def create_event(self, event: EventCreateSchema) -> EventSchema:
        event = await self._repository.create(event.model_dump())
        return EventSchema.model_validate(event, from_attributes=True)

    async def update_event_by_id(
        self, event_id: UUID, new_event: EventUpdateSchema
    ) -> EventSchema:
        event = await self.get_event_by_id(event_id)

        for key, value in new_event.model_dump(exclude_unset=True).items():
            setattr(event, key, value)

        event = await self._repository.update_by_id(event_id, event.model_dump())
        return EventSchema.model_validate(event, from_attributes=True)
    
    async def delete_event_by_id(self, event_id: UUID) -> None:
        message = await self.get_event_by_id(event_id)
        await self._repository.delete_by_id(event_id)
    
    async def get_paginated_events(
        self, start: str, count: int
    ) -> list[EventSchema]:
        offset = 0
        if start != "last":
            try:
                offset = int(start)
                if offset < 0:
                    offset = 0
            except ValueError:
                raise ValueError("start must be a number or 'last'")
        
        events = await self._repository.get_paginated(offset, count)
        return [
            EventSchema.model_validate(event, from_attributes=True) for event in events
        ]
    
    async def get_event_tickets(
        self, event_id: UUID
    ) -> list[TicketSchema]:
        ticket_service = TicketService(self._session)
        tickets = await ticket_service.get_tickets_by_event_id(event_id)
        return tickets
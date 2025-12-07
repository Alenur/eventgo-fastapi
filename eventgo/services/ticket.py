from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.schemas.ticket import (
    TicketSchema,
    TicketCreateSchema,
    TicketUpdateSchema
)
from eventgo.repositories.event import EventRepository
from eventgo.repositories.ticket import TicketRepository
from eventgo.utils.exceptions import NotFoundError


class TicketService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = TicketRepository(session)

    async def get_ticket_by_id(self, ticket_id: UUID) -> TicketSchema:
        ticket = await self._repository.get_by_id(ticket_id)
        if ticket is None:
            raise NotFoundError(f"ticket_id: {ticket_id}")
        return TicketSchema.model_validate(ticket, from_attributes=True)

    async def create_ticket(self, ticket: TicketCreateSchema, event_id: UUID) -> TicketSchema:
        event_repos = EventRepository(self._session)
        event = await event_repos.get_by_id(event_id)
        if event is None:
            raise NotFoundError(f"event with id {event_id} not found")
        ticket_data = ticket.model_dump()
        ticket_data["event_id"] = event_id
        created_ticket = await self._repository.create(ticket_data)
        return TicketSchema.model_validate(created_ticket, from_attributes=True)

    async def update_ticket_by_id(
        self, ticket_id: UUID, new_ticket: TicketUpdateSchema
    ) -> TicketSchema:
        ticket = await self.get_ticket_by_id(ticket_id)

        for key, value in new_ticket.model_dump(exclude_unset=True).items():
            setattr(ticket, key, value)

        ticket = await self._repository.update_by_id(ticket_id, ticket.model_dump())
        return TicketSchema.model_validate(ticket, from_attributes=True)
    
    async def delete_ticket_by_id(self, ticket_id: UUID) -> None:
        ticket = await self.get_ticket_by_id(ticket_id)
        await self._repository.delete_by_id(ticket_id)
    
    async def get_tickets_by_event_id(
        self, event_id: UUID
    ) -> list[TicketSchema]:
        tickets = await self._repository.get_all_by_event_id(event_id)
        if tickets is None:
            raise NotFoundError(f"tickets from {event_id} not found")
        return [
            TicketSchema.model_validate(ticket, from_attributes=True) for ticket in tickets
        ]
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from eventgo.db.models.ticket import Ticket
from eventgo.repositories.base import SQLAlchemyRepository


class TicketRepository(SQLAlchemyRepository):
    model = Ticket

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
    
    async def get_all_by_event_id(self, event_id: UUID):
        stmt = select(self.model).where(self.model.event_id == event_id)
        return await self._session.scalars(stmt)
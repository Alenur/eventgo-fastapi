from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.models.available_ticket import AvailableTicket
from eventgo.repositories.base import SQLAlchemyRepository


class AvailableTicketRepository(SQLAlchemyRepository):
    model = AvailableTicket

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
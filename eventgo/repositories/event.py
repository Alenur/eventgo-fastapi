from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.models.event import Event
from eventgo.repositories.base import SQLAlchemyRepository


class EventRepository(SQLAlchemyRepository):
    model = Event

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
    
    async def get_paginated(
        self, offset: int, limit: int
    ):
        stmt = (
            select(self.model)
            .order_by(desc(self.model.created_at))
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
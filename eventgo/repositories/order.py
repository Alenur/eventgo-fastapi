from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from eventgo.db.models.order import Order
from eventgo.repositories.base import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
    
    async def get_all_by_user_id(self, user_id: UUID) -> list[Order]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        return await self._session.scalars(stmt)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID

from eventgo.db.models.order_item import OrderItem
from eventgo.repositories.base import SQLAlchemyRepository


class OrderItemRepository(SQLAlchemyRepository):
    model = OrderItem

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
    
    async def get_all_by_order_id(self, order_id: UUID):
        stmt = select(self.model).where(self.model.order_id == order_id)
        return await self._session.scalars(stmt)
from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.models.order_item import OrderItem
from eventgo.repositories.base import SQLAlchemyRepository


class OrderItemRepository(SQLAlchemyRepository):
    model = OrderItem

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
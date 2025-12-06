from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.models.order import Order
from eventgo.repositories.base import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
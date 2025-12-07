from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.schemas.order import (
    OrderSchema,
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderDetailSchema
)
from eventgo.db.schemas.order_item import OrderItemDetailSchema
from eventgo.repositories.order import OrderRepository
from eventgo.repositories.user import UserRepository
from eventgo.services.order_item import OrderItemService
from eventgo.utils.exceptions import NotFoundError


class OrderService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = OrderRepository(session)
    
    async def get_order_by_id(self, order_id: UUID) -> OrderDetailSchema:
        order = await self._repository.get_by_id(order_id)
        if order is None:
            raise NotFoundError(f"order_id: {order_id}")
        
        items_service = OrderItemService(self._session)
        items = await items_service.get_items_by_order_id(order_id)
        
        return OrderDetailSchema(
            order_id=order.id,
            status=order.status,
            user_id=order.user_id,
            created_at=order.created_at,
            items=items
        )

    async def create_order(self, order: OrderCreateSchema, user_id: UUID) -> OrderDetailSchema:
        user_repos = UserRepository(self._session)
        user = await user_repos.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"user with id {user_id} not found")
        
        # Создаем заказ без элементов
        order_data = {"status": order.status, "user_id": user_id}
        created_order = await self._repository.create(order_data)
        
        # Создаем элементы заказа
        from eventgo.repositories.order_item import OrderItemRepository
        from eventgo.repositories.base import SQLAlchemyRepository
        from eventgo.db.models.ticket import Ticket
        
        order_item_repo = OrderItemRepository(self._session)
        ticket_repo = SQLAlchemyRepository(self._session)
        ticket_repo.model = Ticket
        
        items_detail = []
        for item_input in order.items:
            # Получаем билет для расчета цены
            ticket = await ticket_repo.get_by_id(item_input.ticket_id)
            if ticket is None:
                raise NotFoundError(f"ticket_id: {item_input.ticket_id}")
            
            # Проверяем доступность билетов
            if ticket.available_count < item_input.quantity:
                raise ValueError(f"Not enough tickets available. Requested: {item_input.quantity}, available: {ticket.available_count}")
            
            # Создаем элемент заказа
            item_data = {
                "order_id": created_order.id,
                "ticket_id": item_input.ticket_id,
                "quantity": item_input.quantity,
                "final_price": ticket.price * item_input.quantity
            }
            await order_item_repo.create(item_data)
            
            # Обновляем количество доступных билетов
            ticket.available_count -= item_input.quantity
            await ticket_repo.update_by_id(ticket.id, {"available_count": ticket.available_count})
            
            # Добавляем в детали
            items_detail.append(
                OrderItemDetailSchema(
                    ticket_id=ticket.id,
                    name=ticket.type,
                    price=ticket.price,
                    quantity=item_input.quantity
                )
            )
        
        return OrderDetailSchema(
            order_id=created_order.id,
            status=created_order.status,
            user_id=created_order.user_id,
            created_at=created_order.created_at,
            items=items_detail
        )
    
    async def delete_order_by_id(self, order_id: UUID) -> None:
        order = await self.get_order_by_id(order_id)
        await self._repository.delete_by_id(order_id)
    
    async def get_orders_by_user_id(
        self, user_id: UUID
    ) -> list[OrderDetailSchema]:
        orders = await self._repository.get_all_by_user_id(user_id)
        if orders is None:
            raise NotFoundError(f"orders from {user_id} not found")
        detail_orders = []
        for order in orders:
            items = order.items
            detail_orders.append(
                OrderDetailSchema(
                    order_id=order.id,
                    status=order.status,
                    user_id=order.user_id,
                    created_at=order.created_at,
                    items=[
                        OrderItemDetailSchema(
                            order_id=item.order_id,
                            ticket_id=item.ticket_id,
                            quantity=item.quantity,
                            name=item.ticket.type,
                            price=item.ticket.price
                        ) for item in items
                    ]
                )
            )
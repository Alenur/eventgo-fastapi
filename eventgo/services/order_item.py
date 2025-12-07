from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from eventgo.db.schemas.order_item import (
    OrderItemSchema,
    OrderItemCreateSchema,
    OrderItemUpdateSchema,
    OrderItemDetailSchema
)
from eventgo.repositories.order import OrderRepository
from eventgo.repositories.order_item import OrderItemRepository
from eventgo.services.ticket import TicketService
from eventgo.utils.exceptions import NotFoundError


class OrderItemService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repository = OrderItemRepository(session)

    async def get_item_by_id(self, item_id: UUID) -> OrderItemDetailSchema:
        item = await self._repository.get_by_id(item_id)
        ticket = item.ticket
        if item is None:
            raise NotFoundError(f"item_id: {item_id}")
        return OrderItemDetailSchema(
            ticket_id=item.ticket_id,
            name=ticket.type,
            price=ticket.price,
            quantity=item.quantity
        )

    async def create_item(self, item: OrderItemCreateSchema, order_id: UUID) -> OrderItemSchema:
        order_repos = OrderRepository(self._session)
        order = await order_repos.get_by_id(order_id)
        if order is None:
            raise NotFoundError(f"order with id {order_id} not found")
        item_data = item.model_dump()
        item_data["order_id"] = order_id
        created_item = await self._repository.create(item_data)
        return OrderItemSchema.model_validate(created_item, from_attributes=True)

    async def update_item_by_id(
        self, item_id: UUID, new_item: OrderItemUpdateSchema
    ) -> OrderItemSchema:
        item = await self.get_item_by_id(item_id)

        for key, value in new_item.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        item = await self._repository.update_by_id(item_id, item.model_dump())
        return OrderItemSchema.model_validate(item, from_attributes=True)
    
    async def delete_item_by_id(self, item_id: UUID) -> None:
        item = await self.get_item_by_id(item_id)
        await self._repository.delete_by_id(item_id)
    
    async def get_items_by_order_id(
        self, order_id: UUID
    ) -> list[OrderItemDetailSchema]:
        items = await self._repository.get_all_by_order_id(order_id)
        if items is None:
            raise NotFoundError(f"items from {order_id} not found")
        detail_items = []
        for item in items:
            ticket = item.ticket
            detail_items.append(
                OrderItemDetailSchema(
                    ticket_id=item.ticket_id,
                    name=ticket.type,
                    price=ticket.price,
                    quantity=item.quantity
                )
            )
        return detail_items
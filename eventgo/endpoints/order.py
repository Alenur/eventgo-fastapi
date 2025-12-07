import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status

from eventgo.db.schemas.order import OrderSchema, OrderDetailSchema, OrderCreateSchema
from eventgo.endpoints.dependencies import OAuth, get_session
from eventgo.services.order import OrderService

router = APIRouter(prefix="/orders")

logger = logging.getLogger(__name__)


@router.post("/", response_model=OrderDetailSchema, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreateSchema,
    oauth: OAuth,
    session=Depends(get_session),
):
    order_service = OrderService(session)
    return await order_service.create_order(order, oauth.id)


@router.get("/{id}", response_model=OrderDetailSchema, status_code=status.HTTP_200_OK)
async def get_order(
    id: UUID,
    oauth: OAuth,
    session=Depends(get_session),
):
    order_service = OrderService(session)
    return await order_service.get_order_by_id(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    id: UUID,
    oauth: OAuth,
    session=Depends(get_session),
):
    order_service = OrderService(session)
    await order_service.delete_order_by_id(id)
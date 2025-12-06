from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from eventgo.db.models.base import Base, TimeStampMixin
from eventgo.utils.enums import OrderStatusType

if TYPE_CHECKING:
    from eventgo.db.models.order_item import OrderItem


class Order(Base, TimeStampMixin):
    __tablename__ = "order"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    status: Mapped[OrderStatusType] = mapped_column(ENUM(OrderStatusType), nullable=False)

    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")

    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"Order({attrs})"

    class Config:
        orm_mode = True
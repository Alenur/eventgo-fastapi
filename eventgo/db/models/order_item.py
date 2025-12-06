from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from eventgo.db.models.base import Base, TimeStampMixin

if TYPE_CHECKING:
    from eventgo.db.models.order import Order


class OrderItem(Base, TimeStampMixin):
    __tablename__ = "order_item"

    order_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("order.id"), nullable=False
    )
    available_ticket_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("available_ticket.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    final_price: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"OrderItem({attrs})"

    class Config:
        orm_mode = True
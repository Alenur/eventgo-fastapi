from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from eventgo.db.models.base import Base, TimeStampMixin
from eventgo.utils.enums import TicketType

if TYPE_CHECKING:
    from eventgo.db.models.event import Event


class AvailableTicket(Base, TimeStampMixin):
    __tablename__ = "available_ticket"

    event_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("event.id"), nullable=False
    )
    type: Mapped[TicketType] = mapped_column(ENUM(TicketType), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    total_count: Mapped[int] = mapped_column(nullable=False)
    available_count: Mapped[int] = mapped_column(nullable=False)

    event: Mapped["Event"] = relationship(back_populates="tickets")

    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"Ticket({attrs})"

    class Config:
        orm_mode = True
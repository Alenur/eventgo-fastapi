from datetime import datetime

from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from eventgo.db.models.base import Base, TimeStampMixin
from eventgo.utils.enums import EventCategory

if TYPE_CHECKING:
    from eventgo.db.models.ticket import Ticket


class Event(Base, TimeStampMixin):
    __tablename__ = "event"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    category: Mapped[EventCategory] = mapped_column(ENUM(EventCategory), nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="event")

    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"Event({attrs})"

    class Config:
        orm_mode = True
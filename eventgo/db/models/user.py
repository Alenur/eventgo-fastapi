from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from eventgo.db.models.base import Base, TimeStampMixin

if TYPE_CHECKING:
    from eventgo.db.models.auth import Auth


class User(Base, TimeStampMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)
    third_name: Mapped[str] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

    auths: Mapped[list["Auth"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"User({attrs})"

    class Config:
        orm_mode = True
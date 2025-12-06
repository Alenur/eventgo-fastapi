from enum import StrEnum


class TokenType(StrEnum):
    access = "access"
    refresh = "refresh"


class EventCategory(StrEnum):
    concert = "concert"
    theater = "theater"
    sport = "sport"
    festival = "festival"


class TicketType(StrEnum):
    vip = "vip"
    standard = "standard"


class OrderStatusType(StrEnum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"

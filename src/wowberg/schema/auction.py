import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base, JsonSerializable


class Auction(Base, JsonSerializable):
    __tablename__ = "auctions"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    quantity: Mapped[int] = mapped_column()
    buyout: Mapped[int] = mapped_column()
    created_on: Mapped[datetime.datetime] = mapped_column()
    last_seen: Mapped[datetime.datetime] = mapped_column()
    prob_is_sold: Mapped[float] = mapped_column(default=0.0)


from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    modifier: Mapped[int] = mapped_column()
    context: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSONB, nullable=True)
    bonus_list: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(JSONB, nullable=True)
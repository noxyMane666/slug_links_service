import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import (
    UUID as ALCHEMY_UUID,
    String,
    DateTime,
    func
)

class Base(DeclarativeBase):
    pass

class ShortURL(Base):
    __tablename__ = "short_urls"

    id: Mapped[UUID] = mapped_column(
        ALCHEMY_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    slug: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )
    long_url: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


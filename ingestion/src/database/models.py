from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class JobModel(Base):

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(500)
    )

    company: Mapped[str] = mapped_column(
        String(300)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    city: Mapped[str] = mapped_column(
        String(200)
    )

    source: Mapped[str] = mapped_column(
        String(100)
    )

    source_url: Mapped[str] = mapped_column(
        Text
    )

    skills: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list
    )

    salary_min: Mapped[int | None]

    salary_max: Mapped[int | None]

    content_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

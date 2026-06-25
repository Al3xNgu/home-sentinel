from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Person(Base):
    """
    Stores known individuals that Home Sentinel can recognize
    """
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    
    # Deleting a person should remove all associated training photos
    photos = relationship(
        "PersonPhoto",
        back_populates="person",
        cascade="all, delete-orphan"
    )

    # Deleting a person should remove all associated embeddings
    embeddings = relationship(
        "FaceEmbedding",
        back_populates="person",
        cascade="all, delete-orphan"
    )
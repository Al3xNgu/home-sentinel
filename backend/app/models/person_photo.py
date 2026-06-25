from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class PersonPhoto(Base):
    """
    Stores uploaded training images for a known person
    """
    __tablename__ = "person_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"),
        nullable=False
    )
    image_path: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    person = relationship(
        "Person",
        back_populates="photos"
    )
    
    # A photo may have multiple embeddings
    embeddings = relationship(
        "FaceEmbedding",
        back_populates="photo",
    )
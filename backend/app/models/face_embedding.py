from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.database import Base


class FaceEmbedding(Base):
    """
    Stores vector representations generated from training photos.
    Used during facial recognition matching
    """
    __tablename__ = "face_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"),
        nullable=False
    )
    photo_id: Mapped[int] = mapped_column(
        ForeignKey("person_photos.id"),
        nullable=False
    )

    # ArcFace produces a 512-dimensional embedding vector.
    embedding: Mapped[list[float]] = mapped_column(
        Vector(512),
        nullable=False
    )

    # Stores the model used to generate the embedding
    model_name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    person = relationship(
        "Person",
        back_populates="embeddings"
    )

    # Each embedding belongs to the photo it was generated from.
    photo = relationship(
        "PersonPhoto",
        back_populates="embeddings"
    )
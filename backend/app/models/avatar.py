import uuid
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Avatar(Base):
    __tablename__ = "avatars"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(20), default="blue")
    # JSON column stores flexible appearance data: hat_id, shirt_id, etc.
    appearance: Mapped[dict] = mapped_column(JSON, default=dict)

    user: Mapped["User"] = relationship("User", back_populates="avatar")
    equipped_items: Mapped[list["InventoryItem"]] = relationship(
        "InventoryItem", primaryjoin="and_(InventoryItem.user_id==Avatar.user_id, InventoryItem.is_equipped==True)",
        foreign_keys="InventoryItem.user_id", viewonly=True
    )
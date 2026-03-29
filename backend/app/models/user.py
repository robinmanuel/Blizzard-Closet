import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, Numeric, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    coin_balance: Mapped[float] = mapped_column(Numeric(12, 2), default=500.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships (defined here, linked in other models)
    avatar: Mapped["Avatar"] = relationship("Avatar", back_populates="user", uselist=False)
    inventory: Mapped[list["InventoryItem"]] = relationship("InventoryItem", back_populates="user")
    sent_trades: Mapped[list["Trade"]] = relationship("Trade", foreign_keys="Trade.sender_id", back_populates="sender")
    received_trades: Mapped[list["Trade"]] = relationship("Trade", foreign_keys="Trade.receiver_id", back_populates="receiver")
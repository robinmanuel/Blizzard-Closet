import uuid
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Numeric, Enum as SAEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base

class TradeStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    cancelled = "cancelled"

class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    receiver_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    sender_coins: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    receiver_coins: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    status: Mapped[TradeStatus] = mapped_column(SAEnum(TradeStatus), default=TradeStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id], back_populates="sent_trades")
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id], back_populates="received_trades")
    # Items offered by each side of the trade
    sender_items: Mapped[list["TradeItem"]] = relationship("TradeItem", foreign_keys="TradeItem.trade_id", primaryjoin="and_(TradeItem.trade_id==Trade.id, TradeItem.side=='sender')")
    receiver_items: Mapped[list["TradeItem"]] = relationship("TradeItem", foreign_keys="TradeItem.trade_id", primaryjoin="and_(TradeItem.trade_id==Trade.id, TradeItem.side=='receiver')")

class TradeItem(Base):
    __tablename__ = "trade_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trades.id"))
    inventory_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.id"))
    side: Mapped[str] = mapped_column(default="sender")  # "sender" or "receiver"
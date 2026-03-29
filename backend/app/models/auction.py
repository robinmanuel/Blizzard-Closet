import uuid
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Numeric, DateTime, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base

class AuctionStatus(str, enum.Enum):
    active = "active"
    closed = "closed"
    cancelled = "cancelled"

class Auction(Base):
    __tablename__ = "auctions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id"))
    inventory_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.id"))
    starting_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    current_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    highest_bidder_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status: Mapped[AuctionStatus] = mapped_column(SAEnum(AuctionStatus), default=AuctionStatus.active)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    seller: Mapped["User"] = relationship("User", foreign_keys=[seller_id])
    highest_bidder: Mapped["User"] = relationship("User", foreign_keys=[highest_bidder_id])
    item: Mapped["Item"] = relationship("Item")
    bids: Mapped[list["Bid"]] = relationship("Bid", back_populates="auction")

class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("auctions.id"))
    bidder_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    placed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    auction: Mapped["Auction"] = relationship("Auction", back_populates="bids")
    bidder: Mapped["User"] = relationship("User")
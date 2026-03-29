import uuid
from sqlalchemy import String, Numeric, Enum as SAEnum, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.core.database import Base

class ItemType(str, enum.Enum):
    hat = "hat"
    shirt = "shirt"
    shoes = "shoes"
    accessory = "accessory"
    background = "background"

class ItemRarity(str, enum.Enum):
    common = "common"
    rare = "rare"
    epic = "epic"
    legendary = "legendary"

class Item(Base):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), default="")
    item_type: Mapped[ItemType] = mapped_column(SAEnum(ItemType), nullable=False)
    rarity: Mapped[ItemRarity] = mapped_column(SAEnum(ItemRarity), default=ItemRarity.common)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), default="")
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    inventory_entries: Mapped[list["InventoryItem"]] = relationship("InventoryItem", back_populates="item")
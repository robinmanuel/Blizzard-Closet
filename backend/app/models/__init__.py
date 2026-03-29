# Import all models so Alembic detects them during migration generation
from app.models.user import User, UserRole
from app.models.avatar import Avatar
from app.models.item import Item, ItemType, ItemRarity
from app.models.inventory import InventoryItem
from app.models.auction import Auction, Bid, AuctionStatus
from app.models.trade import Trade, TradeItem, TradeStatus
from app.models.message import Message

__all__ = [
    "User", "UserRole",
    "Avatar",
    "Item", "ItemType", "ItemRarity",
    "InventoryItem",
    "Auction", "Bid", "AuctionStatus",
    "Trade", "TradeItem", "TradeStatus",
    "Message",
]
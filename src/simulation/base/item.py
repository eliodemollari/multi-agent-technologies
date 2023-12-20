from enum import Enum, auto
from utils import logging_utils


class ItemStatus(Enum):
    AWAITING_PICKUP = auto()
    IN_TRANSIT = auto()
    DELIVERED = auto()


class Item:
    """An item that can be picked up and delivered"""

    def __init__(self, created_tick: int, source: int, destination: int,
                 status: ItemStatus = ItemStatus.AWAITING_PICKUP):
        self.created_tick = created_tick
        self.delivered_tick = None
        self.source = source
        self.destination = destination
        self.status = status

        self.logger = logging_utils.setup_logger("ItemLogger", "item.log")
        self.logger.info(f"Item created with tick {created_tick}, source {source}, destination {destination}, status {status}")

from enum import Enum, auto

import uuid

from src.simulation.base.grid import PickupStation, DeliveryStation
from src.utils import logging_utils


class ItemStatus(Enum):
    ASSIGNED_TO_AGENT = auto()
    AWAITING_PICKUP = auto()
    IN_TRANSIT = auto()
    DELIVERED = auto()


class Item:
    """An item that can be picked up and delivered"""

    def __init__(self, created_tick: int, source: PickupStation, destination: DeliveryStation,
                 status: ItemStatus = ItemStatus.AWAITING_PICKUP):
        self.id = uuid.uuid4()
        self.created_tick = created_tick
        self.pickup_tick = None
        self.delivered_tick = None
        self.agent_id = None
        self.source = source
        self.destination = destination
        self.status = status

        self.logger = logging_utils.setup_logger("ItemLogger", "item.log")
        self.logger.info(f"Item created with tick {created_tick}, source {source}, destination {destination}, status {status}")
        print(f"Item created with tick {created_tick}, source {source}, destination {destination}, status {status}")

    def set_status(self, status: ItemStatus, tick: int):
        self.status = status
        if status == ItemStatus.IN_TRANSIT:
            self.pickup_tick = tick
        elif status == ItemStatus.DELIVERED:
            self.delivered_tick = tick

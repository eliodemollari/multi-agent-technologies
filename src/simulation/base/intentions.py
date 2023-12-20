from abc import ABC

from utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('IntentionsLogger', 'intentions.log')


class Intention(ABC):
    """An intention is an atomic action that the agent would like to perform
    during single round"""

    def __init__(self, made_by: int):
        self.made_by = made_by
        logger.info(f"Intention initialized by agent {made_by}")


class Pickup(Intention):
    """An intention to pick up an item from the pickup station that the agent is on"""

    def __init__(self, made_by: int, item_id: int | None = None):
        """:param int | None item_id: None means that the agent wants to pick up any item"""
        super().__init__(made_by)
        self.item_id = item_id
        logger.info(f"Pickup intention initialized by agent {made_by} for item {item_id}")


class Deliver(Intention):
    """An intention to deliver an item to a delivery station that the agent is on"""
    pass


class Move(Intention):
    """An intention to move to a new position expressed by a vector"""

    def __init__(self, made_by: int, new_position: tuple[int, int]):
        super().__init__(made_by)
        self.new_position = new_position
        logger.info(f"Move intention initialized by agent {made_by} to position {new_position}")

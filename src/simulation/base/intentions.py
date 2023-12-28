from abc import ABC

from src.utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('IntentionsLogger', 'intentions.log')


class Intention(ABC):
    """An intention is an atomic action that the agent would like to perform
    during single round"""

    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        logger.info(f"Intention initialized by agent {agent_id}")


class Pickup(Intention):
    """An intention to pick up an item from the pickup station that the agent is on"""

    def __init__(self, agent_id: int, item_id: int):
        """:param int | None item_id: None means that the agent wants to pick up any item"""
        super().__init__(agent_id)
        self.item_id = item_id
        logger.info(f"Pickup intention initialized by agent {agent_id} for item {item_id}")


class Deliver(Intention):
    """An intention to deliver an item to a delivery station that the agent is on"""

    def __init__(self, agent_id: int, item_id: int | None = None):
        """:param int | None item_id: None means that the agent wants to pick up any item"""
        super().__init__(agent_id)
        self.item_id = item_id
        logger.info(f"Delivery intention initialized by agent {agent_id} for item {item_id}")


class Move(Intention):
    """An intention to move to a new position expressed by a vector"""

    # Define allowed moves
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    ALLOWED_MOVES = {LEFT, RIGHT, UP, DOWN}

    def __init__(self, agent_id: int, direction: tuple[int, int]):
        super().__init__(agent_id)
        if direction not in self.ALLOWED_MOVES:
            raise ValueError(f"Invalid move direction: {direction}. Allowed directions are {self.ALLOWED_MOVES}")
        self.direction = direction
        logger.info(f"Move intention initialized by agent {agent_id} to direction {direction}")

from abc import ABC, abstractmethod

from simulation.base.intentions import Intention
from simulation.base.item import Item
from utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('GridLogger', 'grid.log')


def find_element_in_grid(grid: 'Grid', element: type['BoardObject']) -> tuple[int, int] | None:
    """Find the 2D coordinates of an element in the grid"""
    for x, row in enumerate(grid.board):
        for y, cell in enumerate(row):
            if element in cell:
                return x, y

    logger.info(f"Element {element} not found in grid")
    return None


def create_empty_board(dim_x: int, dim_y: int) -> list[list[list['BoardObject']]]:
    return [[[] for _ in range(dim_y)] for _ in range(dim_x)]


class InvalidGrid(Exception):
    """Generic exception for grids that do not match pre-established contracts"""
    pass


class BoardObject(ABC):
    pass


class Obstacle(BoardObject):
    pass


class Station(BoardObject, ABC):
    pass


class DeliveryStation(Station):
    pass


class PickupStation(Station):
    def __init__(self, to_collect: list[Item] | None = None):
        self.to_collect = to_collect if to_collect is not None else []


class Agent(BoardObject, ABC):
    def __init__(self):
        self.items = []

    @abstractmethod
    def make_intention(self, grid: 'Grid') -> Intention:
        pass


class Grid:
    def __init__(self, pickup_stations: dict[int, PickupStation], delivery_stations: dict[int, DeliveryStation],
                 agents: dict[int, Agent], board: list[list[list[BoardObject]]]):
        self.pickup_stations = pickup_stations
        self.delivery_stations = delivery_stations
        self.agents = agents
        self.board = board

    def board_dimensions(self) -> tuple[int, int]:
        return len(self.board), len(self.board[0])

    def add_board_object(self, obj: BoardObject, position: tuple[int, int]):
        x, y = position
        self.board[x][y].append(obj)
        logger.info(f"Added {obj} to grid at position {position}")

    def remove_board_object(self, obj: BoardObject, position: tuple[int, int]):
        x, y = position
        self.board[x][y].remove(obj)

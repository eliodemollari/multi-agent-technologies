from abc import ABC, abstractmethod
import uuid

from src.simulation.base.intentions import Intention
from src.utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('GridLogger', 'grid.log')


def create_empty_board(dim_x: int, dim_y: int) -> list[list[list['BoardObject']]]:
    return [[[] for _ in range(dim_y)] for _ in range(dim_x)]


class InvalidGrid(Exception):
    """Generic exception for grids that do not match pre-established contracts"""
    pass


class BoardObject(ABC):
    def __init__(self):
        self.id = uuid.uuid4()
        self.position = None

    def set_position(self, position: tuple[int, int]):
        self.position = position

    def get_position(self) -> tuple[int, int]:
        return self.position


class Obstacle(BoardObject):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.set_position(position)


class DeliveryStation(BoardObject, ABC):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.set_position(position)
        self.items = []  # List of items at the station


class PickupStation(BoardObject, ABC):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.set_position(position)
        self.items = []  # List of items at the station


class Agent(BoardObject, ABC):
    def __init__(self, position: tuple[int, int], capacity: int = 1):
        super().__init__()
        self.set_position(position)
        self.items = []
        self.capacity = capacity

    @abstractmethod
    def make_intention(self, grid: 'Grid') -> Intention:
        pass


class Grid:
    def __init__(self, board: list[list[list[BoardObject]]],
                 grid_size: [int, int],
                 pickup_stations: list[PickupStation] = None,
                 delivery_stations: list[DeliveryStation] = None,
                 obstacles: list[Obstacle] = None,
                 agents: dict[int, Agent] = None):
        self.pickup_stations = pickup_stations if pickup_stations is not None else []
        self.delivery_stations = delivery_stations if delivery_stations is not None else []
        self.obstacles = obstacles if obstacles is not None else []
        self.agents = agents if agents is not None else []
        self.board = board
        self.grid_size = grid_size

    def board_dimensions(self) -> tuple[int, int]:
        return len(self.board), len(self.board[0])

    def add_board_object(self, obj: BoardObject):
        x, y = obj.position
        self.board[x][y].append(obj)

        # Check the type of the object and add it to the appropriate list
        if isinstance(obj, PickupStation):
            self.pickup_stations.append(obj)
        elif isinstance(obj, DeliveryStation):
            self.delivery_stations.append(obj)
        elif isinstance(obj, Agent):
            self.agents.append(obj)
        elif isinstance(obj, Obstacle):
            self.obstacles.append(obj)
        else:
            raise InvalidGrid(f"Object {obj} of type {type(obj)} is not a valid board object")

        logger.info(f"Added {obj} to grid at position {obj.position}")
        print(f"Added {obj} to grid at position {obj.position}")

    def remove_board_object(self, obj: BoardObject, position: tuple[int, int]):
        x, y = position
        self.board[x][y].remove(obj)

    def get_most_crowded_pickup_station(self):
        pickup_stations_sorted_by_crowd = sorted(self.pickup_stations, key=lambda station: len(station.items),
                                                 reverse=True)
        most_crowded_station = pickup_stations_sorted_by_crowd[0] if pickup_stations_sorted_by_crowd else None
        return most_crowded_station

    def get_agent_index_by_id(self, agent_id):
        return next((index for index, agent in enumerate(self.agents) if agent.id == agent_id), None)

    def get_pickup_station_index_by_id(self, station_id):
        return next((index for index, station in enumerate(self.pickup_stations) if station.id == station_id), None)

    def get_delivery_station_index_by_id(self, station_id):
        return next((index for index, station in enumerate(self.delivery_stations) if station.id == station_id), None)

    def get_obstacle_index_by_id(self, obstacle_id):
        return next((index for index, obstacle in enumerate(self.obstacles) if obstacle.id == obstacle_id), None)

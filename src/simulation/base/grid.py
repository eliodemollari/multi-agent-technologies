import random
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
    def __init__(self, position: tuple[int, int], broker_instance=None):
        super().__init__()
        self.set_position(position)
        self.items = []  # List of items at the station
        self.broker = broker_instance

    # Add item to pickup station
    def add_item(self, item):
        print(f"Adding item {item} to pickup station {self.id}")
        logger.info(f"Adding item {item} to pickup station {self.id}")
        self.items.append(item)
        self.request_agents(item)

    # Remove item from pickup station
    def remove_item(self, item):
        self.items.remove(item)

    # Contact the broker to request agents availability
    def request_agents(self, item):
        # Pickup station requests available agents from the broker
        print(f"Pickup Station {self} requesting available agents for item {item} from broker")
        logger.info(f"Pickup Station {self} requesting available agents for item {item} from broker")
        available_agents = self.broker.recommend_agents(item)
        return available_agents

    # Select an agent from the list of available agents by assigning the item to the agent
    @staticmethod
    def select_agent(available_agents, item):
        # Randomly select an agent from the list of available agents
        print(f"Pickup Station selecting agent for item {item}")
        logger.info(f"Pickup Station selecting agent for item {item}")
        random_index = random.randint(0, len(available_agents) - 1)
        agent = available_agents[random_index]
        agent.mark_item_as_assigned(item)


class Agent(BoardObject, ABC):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.set_position(position)
        self.items = []

    @abstractmethod
    def make_intention(self, grid: 'Grid') -> Intention:
        pass


class Grid:
    def __init__(self, board: list[list[list[BoardObject]]],
                 pickup_stations: list[PickupStation] = None,
                 delivery_stations: list[DeliveryStation] = None,
                 obstacles: list[Obstacle] = None,
                 agents: dict[int, Agent] = None):
        self.pickup_stations = pickup_stations if pickup_stations is not None else []
        self.delivery_stations = delivery_stations if delivery_stations is not None else []
        self.obstacles = obstacles if obstacles is not None else []
        self.agents = agents if agents is not None else []
        self.board = board

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

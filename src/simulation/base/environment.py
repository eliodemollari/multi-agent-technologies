from abc import ABC, abstractmethod
from src.simulation.base.grid import Grid, Agent
from src.simulation.base.intentions import Intention
from src.simulation.base.item import Item, ItemStatus
from src.utils import logging_utils
import random

# setup logger
logger = logging_utils.setup_logger('EnvironmentLogger', 'environment.log')

def generate_items(pickup_station, delivery_station, created_tick, max_items):
    logger.info(f"Generating items for pickup station {pickup_station.id} and delivery station {delivery_station.id}")
    num_items = random.randint(1, max_items)
    for _ in range(num_items):
        item = Item(
            status=ItemStatus.AWAITING_PICKUP,
            created_tick=created_tick,
            source=pickup_station,
            destination=delivery_station
        )
        pickup_station.items.append(item)
    logger.info(f"{num_items} items added to pickup station {pickup_station.id}")

def _get_intentions(state: Grid) -> list[Intention]:
    list_of_intentions = []
    for agent in state.agents:
        list_of_intentions.append(agent.make_intention(state))
    return list_of_intentions


class Environment(ABC):
    def __init__(self, state: Grid):
        self.state = state
        self.tick = 0

    @abstractmethod
    def _illegal_intentions(self, intentions: list[Intention], state: Grid) -> None:
        pass

    @abstractmethod
    def _contradicting_intentions(self, intentions: list[Intention], state: Grid) -> list[Intention]:
        pass

    @abstractmethod
    def _enact_valid_intentions(self, consistent_intentions: list[Intention], state: Grid) -> Grid:
        pass

    def _process_intentions(self, state: Grid) -> Grid:
        """Iteratively process all intentions in the state, until all agents had their Intention enacted. An important
        assumption is that the number of inconsistent operations ALWAYS eventually falls to 0, as in the conflict
        situation, the Environment will always prefer one of them and realise its wish."""

        new_intentions = _get_intentions(state)

        try:
            self._illegal_intentions(new_intentions, state)
        except Exception as e:
            logger.error(f"Illegal intention detected: {e}")
            raise

        inconsistent_intentions = self._contradicting_intentions(new_intentions, state)
        consistent_intentions = [intention for intention in new_intentions if intention
                                 not in inconsistent_intentions]
        state = self._enact_valid_intentions(consistent_intentions, state)

        return state

    def simulation_step(self) -> Grid:
        random_pickup_station = random.randint(0, len(self.state.pickup_stations) - 1)
        random_delivery_station = random.randint(0, len(self.state.delivery_stations) - 1)
        generate_items(self.state.pickup_stations[random_pickup_station],
                       self.state.delivery_stations[random_delivery_station], self.tick, 1)
        self.state = self._process_intentions(self.state)
        self.tick += 1

        logger.info(f"Simulation step completed at tick {self.tick}")

        return self.state

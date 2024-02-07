from abc import ABC, abstractmethod
from src.simulation.base.grid import Grid, Agent
from src.simulation.base.intentions import Intention
from src.simulation.environments.broker import Broker
from src.utils import logging_utils
from src.simulation.base.item import Item, ItemStatus
import random

# setup logger
logger = logging_utils.setup_logger('EnvironmentLogger', 'environment.log')


def generate_items(pickup_station, delivery_station, created_tick, max_items):
    logger.info(f"Generating items for pickup station {pickup_station.id} and delivery station {delivery_station.id}")
    print(f"Generating items for pickup station {pickup_station.id} and delivery station {delivery_station.id}")
    for _ in range(max_items):
        item = Item(
            status=ItemStatus.AWAITING_PICKUP,
            created_tick=created_tick,
            source=pickup_station,
            destination=delivery_station
        )
        pickup_station.items.append(item)
    logger.info(f"{max_items} items added to pickup station {pickup_station.id}")
    print(f"{max_items} items added to pickup station {pickup_station.id}")


def _get_intentions(state: Grid, selfishness: bool) -> list[Intention]:
    list_of_intentions = []
    for agent in state.agents:
        if agent.is_assigned_item or agent.is_carrying_item:
            list_of_intentions.append(agent.make_intention(state, selfishness))
    return list_of_intentions


class Environment(ABC):
    def __init__(self, state: Grid):
        self.state = state
        self.tick = 0
        self.items_added = 0
        self.pickup_station_counter = 0
        self.delivery_station_counter = 0

    @abstractmethod
    def _illegal_intentions(self, intentions: list[Intention], state: Grid) -> None:
        pass

    @abstractmethod
    def _contradicting_intentions(self, intentions: list[Intention], state: Grid) -> list[Intention]:
        pass

    @abstractmethod
    def _enact_valid_intentions(self, consistent_intentions: list[Intention], state: Grid, tick: int) -> Grid:
        pass

    def _process_intentions(self, state: Grid, tick: int, selfishness: bool) -> Grid:
        """Iteratively process all intentions in the state, until all agents had their Intention enacted. An important
        assumption is that the number of inconsistent operations ALWAYS eventually falls to 0, as in the conflict
        situation, the Environment will always prefer one of them and realise its wish."""

        broker = Broker(state)
        broker.assign_items_to_agents()

        new_intentions = _get_intentions(state, selfishness)

        try:
            self._illegal_intentions(new_intentions, state)
        except Exception as e:
            logger.error(f"Illegal intention detected: {e}")
            raise

        inconsistent_intentions = self._contradicting_intentions(new_intentions, state)
        consistent_intentions = [intention for intention in new_intentions if intention
                                 not in inconsistent_intentions]
        state = self._enact_valid_intentions(consistent_intentions, state, tick)

        return state

    def simulation_step(self, selfishness: bool) -> Grid:
        print('-------------------------------------------------------------------------------------------')
        print(f"Simulation step started at tick {self.tick}")
        # Initialize counters for pickup and delivery stations
        self.pickup_station_counter = 0
        self.delivery_station_counter = 0

        # In your simulation_step method
        if self.items_added < 35 and self.tick != 0:
            # Use the counters to select the stations
            pickup_station = self.state.pickup_stations[self.pickup_station_counter]
            delivery_station = self.state.delivery_stations[self.delivery_station_counter]

            # Generate the items
            generate_items(pickup_station, delivery_station, self.tick, 1)
            self.items_added += 1

            # Update the counters
            self.pickup_station_counter = (self.pickup_station_counter + 1) % len(self.state.pickup_stations)
            self.delivery_station_counter = (self.delivery_station_counter + 1) % len(self.state.delivery_stations)
        self.state = self._process_intentions(self.state, self.tick, selfishness)
        logger.info(f"Simulation step completed at tick {self.tick}")
        print(f"Simulation step completed at tick {self.tick}")
        print('-------------------------------------------------------------------------------------------')
        self.tick += 1

        return self.state

from typing import Any

from src.simulation.base.grid import Grid, Agent, PickupStation, DeliveryStation
from src.simulation.base.intentions import Intention, Move, Pickup, Deliver
from src.simulation.base.item import ItemStatus, Item
from src.simulation.pathfinding import find_shortest_path
from src.utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('ReactiveAgentLogger', 'reactive_agent.log')


class TopCongestionAgent(Agent):
    def __init__(self, position: tuple[int, int]):
        super().__init__(position)

    @property
    def is_carrying_item(self) -> bool:
        return any(item.status == ItemStatus.IN_TRANSIT for item in self.items)

    def get_carried_item(self) -> Any | None:
        for item in self.items:
            if item.status == ItemStatus.IN_TRANSIT:
                return item
        return None

    def is_on_pickup_station(self, grid: Grid) -> PickupStation | None:
        for pickup_station in grid.pickup_stations:
            if pickup_station.position == self.position:
                return pickup_station
        return None

    def update_position(self, new_position: tuple[int, int]):
        self.position = new_position

    def is_on_delivery_station(self, grid: Grid) -> DeliveryStation | None:
        for delivery_station in grid.delivery_stations:
            if delivery_station.position == self.position:
                return delivery_station
        return None

    def make_intention(self, grid: Grid) -> Intention:
        # When Agent is carrying an item
        if self.is_carrying_item:
            item_to_deliver = self.get_carried_item()
            destination_station_position = item_to_deliver.destination.position

            # If the agent carrying on an item and is on a DeliveryStation, deliver the item
            if destination_station_position == self.position:
                logger.info(f"Agent {self.id} is delivering an item")  # log info message
                return Deliver(self.id)
            # If the agent is carrying an item and is not on a DeliveryStation, move towards the destination
            else:
                next_node = find_shortest_path(
                    grid,
                    grid.board_dimensions(),
                    grid.obstacles, self.position,
                    destination_station_position,
                    item_to_deliver.source,
                    item_to_deliver.destination
                )
                # ... existing code to find the path to the target station ...
                logger.info(f"Agent {self.id} is moving towards the target station")  # log info message
                return Move(self.id, (next_node[0] - self.position[0], next_node[1] - self.position[1]))

        # When Agent is not carrying an item
        else:
            # If the agent is not carrying an item and is on a PickupStation, pick up an item
            target_station = grid.get_most_crowded_pickup_station()
            target_station_position = target_station.position
            if target_station_position == self.position:
                logger.info(f"Agent {self.id} is picking up an item")  # log info message
                item = target_station.items[0]
                return Pickup(self.id, item.id)
            # If the agent is not carrying an item and is not on a PickupStation, move towards the target station
            else:
                next_node = find_shortest_path(
                    grid,
                    grid.board_dimensions(),
                    grid.obstacles,
                    self.position,
                    target_station_position,
                    target_station_position
                )
                logger.info(f"Agent {self.id} is moving towards the target station")  # log info message
                return Move(self.id, (next_node[0] - self.position[0], next_node[1] - self.position[1]))

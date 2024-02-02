from typing import Any
from itertools import combinations

from src.simulation.base.grid import Grid, Agent, PickupStation, DeliveryStation
from src.simulation.base.intentions import Intention, Move, Pickup, Deliver
from src.simulation.base.item import ItemStatus, Item
from src.simulation.pathfinding import find_shortest_path, tsp_path
from src.utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('ReactiveAgentLogger', 'reactive_agent.log')


class ItemPath:
    def __init__(self, item, path_length):
        self.item = item
        self.path_length = path_length


class TopCongestionAgent(Agent):
    def __init__(self, position: tuple[int, int], capacity: int = 1):
        super().__init__(position, capacity)

    @property
    def is_carrying_item(self) -> bool:
        return any(item.status == ItemStatus.IN_TRANSIT for item in self.items)

    @property
    def is_assigned_item(self) -> bool:
        return any(item.status == ItemStatus.ASSIGNED_TO_AGENT for item in self.items)

    @property
    def number_of_items_in_transit(self) -> int:
        return sum(1 for item in self.items if item.status == ItemStatus.IN_TRANSIT)

    @property
    def number_of_items_assigned_to_agent(self) -> int:
        return sum(1 for item in self.items if item.status == ItemStatus.ASSIGNED_TO_AGENT)

    @property
    def current_capacity(self) -> int:
        return self.capacity - self.number_of_items_in_transit - self.number_of_items_assigned_to_agent

    def agent_tsp_solution(self, bundle, state: Grid):
        bundle = list(bundle)
        paths_to_items = []
        visited_nodes = []
        total_path_length = 0
        current_position = self.position

        while bundle:
            # Calculate paths to all items in the bundle
            for item in bundle:
                path_to_item = tsp_path(state, current_position, item.source.position)
                paths_to_items.append(ItemPath(item, len(path_to_item) - 1)) # -1 because the path includes the current position

            # Sort paths by length
            paths_to_items.sort(key=lambda item_path: item_path.path_length)

            # The next node to visit is the one with the shortest path
            next_node = paths_to_items[0].item

            # Update total path length
            total_path_length += paths_to_items[0].path_length

            # Remove the item from the bundle and the path from the path list
            bundle.remove(next_node)
            paths_to_items.clear()

            # Update current position to the position of the next node
            current_position = next_node.source.position

            # Add the visited node to the list
            visited_nodes.append(next_node.source.position)

        return visited_nodes, total_path_length

    # Get the list of items and returns the list of bundles
    def receive_auction_information(self, available_items: list[Item], state: Grid):
        bundle = []
        for i in range(1, len(available_items) + 1):
            for subset in combinations(available_items, i):
                if self.current_capacity >= len(subset):
                    visited_nodes, total_path_length = self.agent_tsp_solution(subset, state)
                    obj = {
                        "ordered_bundle": visited_nodes,
                        "costs": total_path_length
                    }
                    bundle.append(obj)
        return bundle

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
                logger.info(f"Agent {self.id} is delivering item {item_to_deliver.id}")  # log info message
                print(f"Agent {self.id} is delivering item {item_to_deliver.id}")
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
                logger.info(f"Agent {self.id} is moving towards the target station position in "
                            f"{destination_station_position}")
                print(f"Agent {self.id} is moving towards the target station position in {destination_station_position}")
                return Move(self.id, (next_node[0] - self.position[0], next_node[1] - self.position[1]))

        # When Agent is not carrying an item
        else:
            # If the agent is not carrying an item and is on a PickupStation, pick up the item assigned to the agent
            # target_station = grid.get_most_crowded_pickup_station()
            # target_station_position = target_station.position

            # Filter the item in agent items list that has status assigned_to_agent
            item_to_pickup = next((item for item in self.items if item.status is ItemStatus.ASSIGNED_TO_AGENT), None)

            target_station_position = item_to_pickup.source.position

            if target_station_position == self.position:
                logger.info(f"Agent {self.id} is picking up an item at the pickup station position in "
                            f"{target_station_position}")
                print(f"Agent {self.id} is picking up an item at the pickup station "
                      f"position in {target_station_position}")
                return Pickup(self.id, item_to_pickup.id)
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
                print(f"Agent {self.id} is moving towards the target station")
                return Move(self.id, (next_node[0] - self.position[0], next_node[1] - self.position[1]))

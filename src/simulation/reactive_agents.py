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

    @property
    def no_more_items_to_pickup(self) -> bool:
        return not any(item.status == ItemStatus.ASSIGNED_TO_AGENT for item in self.items)

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
            visited_nodes.append(next_node)

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
                        "costs": round(total_path_length / self.capacity),
                        "agent": self
                    }
                    bundle.append(obj)
        return bundle

    def get_carried_items(self) -> Any | None:
        items_in_transit = [item for item in self.items if item.status == ItemStatus.IN_TRANSIT]
        return items_in_transit

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

    def make_intention(self, grid: Grid, selfishness) -> Intention:
        if self.no_more_items_to_pickup:
            items_in_transit = self.get_carried_items()

            # Sort the items based on their priority in ascending order
            sorted_items = sorted(items_in_transit, key=lambda item: item.priority)

            # The item with the highest priority will be at the beginning of the list
            highest_priority_item = sorted_items[0]
            destination_station_position = highest_priority_item.destination.position

            # If the agent carrying on an item and is on a DeliveryStation, deliver the item
            if destination_station_position == self.position:
                logger.info(f"Agent {self.id} is delivering item {highest_priority_item.id}")  # log info message
                print(f"Agent {self.id} is delivering item {highest_priority_item.id}")
                return Deliver(self.id, highest_priority_item.id)
            # If the agent is carrying an item and is not on a DeliveryStation, move towards the destination
            else:
                next_node = find_shortest_path(grid, self.position, destination_station_position)
                # ... existing code to find the path to the target station ...
                logger.info(f"Agent {self.id} is moving towards the DS position in {destination_station_position}")
                print(f"Agent {self.id} is moving towards the DS position in {destination_station_position}")
                return Move(self.id, (next_node[0] - self.position[0], next_node[1] - self.position[1]))

        # If there are still items to pick up
        else:
            items_assigned = [item for item in self.items if item.status == ItemStatus.ASSIGNED_TO_AGENT]

            # Sort the items based on their priority in ascending order
            sorted_items = sorted(items_assigned, key=lambda item: item.priority)

            # The item with the highest priority will be at the beginning of the list
            highest_priority_item = sorted_items[0]
            target_station_position = highest_priority_item.source.position

            # If agent on a PickupStation of an assigned item, pick up the item
            if target_station_position == self.position:
                logger.info(f"Agent {self.id} is picking up an item at the pickup station position in "
                            f"{target_station_position}")
                print(f"Agent {self.id} is picking up an item at the pickup station "
                      f"position in {target_station_position}")
                return Pickup(self.id, highest_priority_item.id)
            # If the agent is not on a PickupStation of an assigned, move towards the target station
            else:
                next_node = find_shortest_path(grid, self.position, target_station_position)
                logger.info(f"Agent {self.id} is moving towards the target station")  # log info message
                print(f"Agent {self.id} is moving towards the target station")
                return Move(self.id, (next_node[0] - self.position[0], next_node[1] - self.position[1]))

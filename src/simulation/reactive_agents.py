from simulation.base.grid import Grid, Agent, Station, find_element_in_grid, Obstacle
from simulation.base.intentions import Intention, Move, Pickup, Deliver
from simulation.base.item import ItemStatus
from simulation.pathfinding import find_shortest_path
from utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('ReactiveAgentLogger', 'reactive_agent.log')


class TopCongestionAgent(Agent):
    def __init__(self, n=1):
        super().__init__()
        self.n = n

    @property
    def carrying_item(self) -> bool:
        return any(item.status == ItemStatus.IN_TRANSIT for item in self.items)

    def make_intention(self, grid: Grid) -> Intention:
        # Get the object at the agent's current position
        cell = find_element_in_grid(grid, self)

        # Find agent in grid.agents by value
        agent_id = next(agent_id for agent_id, agent in grid.agents.items() if agent is self)
        obstacles = [(x, y) for x, _ in enumerate(grid.board) for y, cell in enumerate(grid.board[x])
                     if any((isinstance(board_object, Obstacle) for board_object in grid.board[x][y]))]

        if self.carrying_item:
            # If the agent is carrying an item and is on the target DeliveryStation, deliver the item
            item_to_deliver = next(item for item in self.items if item.status == ItemStatus.IN_TRANSIT)
            target_station = grid.delivery_stations[item_to_deliver.destination]
            target_station_position = find_element_in_grid(grid, target_station)
            if target_station_position == cell:
                logger.info(f"Agent {agent_id} is delivering an item")  # log info message
                return Deliver(agent_id)
            # If the agent is carrying an item and is not on a DeliveryStation, move towards the target station
            else:
                next_node = find_shortest_path(grid.board_dimensions(), obstacles, cell, target_station_position)
                # ... existing code to find the path to the target station ...
                logger.info(f"Agent {agent_id} is moving towards the target station")  # log info message
                return Move(agent_id, (next_node[0] - cell[0], next_node[1] - cell[1]))

        else:
            # If the agent is not carrying an item and is on a PickupStation, pick up an item
            # Get all stations
            stations = grid.pickup_stations
            pickup_stations_sorted_by_crowd = {k: v for k, v
                                               in sorted(stations.items(), key=lambda item: len(item[1].to_collect),
                                                         reverse=True)}
            most_crowded_stations = list(pickup_stations_sorted_by_crowd.values())
            target_station: Station = most_crowded_stations[min(len(most_crowded_stations) - 1, self.n)]

            target_station_position = find_element_in_grid(grid, target_station)
            if target_station_position == cell:
                logger.info(f"Agent {agent_id} is picking up an item")  # log info message
                return Pickup(agent_id)
            # If the agent is not carrying an item and is not on a PickupStation, move towards the target station
            else:
                next_node = find_shortest_path(grid.board_dimensions(), obstacles, cell, target_station_position)
                logger.info(f"Agent {agent_id} is moving towards the target station")  # log info message
                return Move(agent_id, (next_node[0] - cell[0], next_node[1] - cell[1]))

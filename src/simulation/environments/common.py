import random
from collections import defaultdict

from simulation.base.grid import Grid, find_element_in_grid, InvalidGrid, PickupStation
from simulation.base.intentions import Move, Intention, Pickup


class IllegalIntention(Exception):
    pass


class IllegalMove(IllegalIntention):
    pass


class IllegalPickup(IllegalIntention):
    pass


class IllegalDelivery(IllegalIntention):
    pass


class UnsupportedIntention(IllegalIntention):
    pass


def find_position_after_move(move_intention: Move, state: Grid) -> tuple[int, int]:
    x, y = find_element_in_grid(state, state.agents[move_intention.made_by])
    return x + move_intention.new_position[0], y + move_intention.new_position[1]


def check_for_out_of_bounds_moves(intentions: list[Intention], state: Grid) -> None:
    move_intentions = filter(lambda intention: isinstance(intention, Move), intentions)
    dim_x, dim_y = state.board_dimensions()

    for move_intention in move_intentions:
        new_x, new_y = find_position_after_move(move_intention, state)
        # Check if the new position is out of bounds
        if new_x < 0 or new_x >= dim_x or new_y < 0 or new_y >= dim_y:
            raise IllegalMove(f"Agent {move_intention.made_by} tried to move out of bounds")


def enact_move_intention(move_intention: Move, state: Grid) -> Grid:
    new_x, new_y = find_position_after_move(move_intention, state)
    # Remove the agent from its current position
    x, y = find_element_in_grid(state, state.agents[move_intention.made_by])
    state.board[x][y].remove(state.agents[move_intention.made_by])
    # Add the agent to its new position
    state.board[new_x][new_y].append(state.agents[move_intention.made_by])

    return state


def group_intentions_by_item_to_pickup(to_group: list[Pickup], state: Grid) -> \
        dict[int, dict[int | None, list[Pickup]]]:
    """Group pickup intentions by pickup station id and item id inside the pickup station"""
    grouped_intentions = defaultdict(lambda: defaultdict(list))

    for intention in to_group:
        location_of_agent = find_element_in_grid(state, state.agents[intention.made_by])
        pickup_station = next((board_object for board_object in
                               state.board[location_of_agent[0]][location_of_agent[1]]
                               if isinstance(board_object, PickupStation)))
        # Find pickup_station in dictionary in Grid
        try:
            pickup_station_id = next((station_id for station_id, station in state.pickup_stations.items()
                                      if station == pickup_station))
        except StopIteration:
            raise InvalidGrid(f"Pickup station from location {location_of_agent} not found in grid")
        grouped_intentions[pickup_station_id][intention.item_id].append(intention)

    return grouped_intentions


def shuffle_grouped_pickup_intentions(grouped_intentions: dict[int, dict[int, list[Pickup]]]) \
        -> dict[int, dict[int, list[Pickup]]]:
    """Shuffle the order of intentions for all requests inside an item entry, so the arbitrary preference is not given
    to the agents who got their intention handled first in previous part of the process, for example thanks to their
    lower id"""
    for pickup_station_id, item_intentions in grouped_intentions.items():
        for item_id, intentions in item_intentions.items():
            random.shuffle(intentions)

    return grouped_intentions

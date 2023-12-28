import random
from collections import defaultdict

from src.simulation.base.grid import Grid, InvalidGrid, PickupStation
from src.simulation.base.intentions import Move, Intention, Pickup

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
    agent = state.get_agent_index_by_id(move_intention.agent_id)
    agent_position = state.agents[agent].position

    x, y = agent_position
    return x + move_intention.direction[0], y + move_intention.direction[1]


def check_for_out_of_bounds_moves(intentions: list[Intention], state: Grid) -> None:
    move_intentions = filter(lambda intention: isinstance(intention, Move), intentions)
    dim_x, dim_y = state.board_dimensions()

    for move_intention in move_intentions:
        new_x, new_y = find_position_after_move(move_intention, state)
        # Check if the new position is out of bounds
        if new_x < 0 or new_x >= dim_x or new_y < 0 or new_y >= dim_y:
            raise IllegalMove(f"Agent {move_intention.agent_id} tried to move out of bounds")


def enact_move_intention(move_intention: Move, state: Grid) -> Grid:
    new_x, new_y = find_position_after_move(move_intention, state)
    # Remove the agent from its current position
    agent_index = state.get_agent_index_by_id(move_intention.agent_id)
    x, y = state.agents[agent_index].position
    state.remove_board_object(state.agents[agent_index], (x, y))
    # Add the agent to its new position
    state.board[new_x][new_y].append(state.agents[agent_index])
    state.agents[agent_index].update_position([new_x, new_y])

    return state


def group_intentions_by_item_to_pickup(to_group: list[Pickup], state: Grid) -> \
        dict[int, dict[int | None, list[Pickup]]]:
    """Group pickup intentions by pickup station id and item id inside the pickup station"""
    grouped_intentions = defaultdict(lambda: defaultdict(list))

    for intention in to_group:
        agent_index = state.get_agent_index_by_id(intention.agent_id)
        agent = state.agents[agent_index]
        pickup_station = agent.is_on_pickup_station(state)
        if pickup_station is None:
            raise IllegalPickup(f"Pickup station from location {agent.position} not found in grid")

        grouped_intentions[pickup_station.id][intention.item_id].append(intention)

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

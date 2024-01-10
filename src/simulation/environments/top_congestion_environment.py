from src.simulation.base.environment import Environment
from src.simulation.base.grid import Grid, Obstacle, PickupStation, DeliveryStation
from src.simulation.base.intentions import Intention, Move, Pickup, Deliver
from src.simulation.base.item import ItemStatus
from src.simulation.environments.common import IllegalIntention, IllegalMove, IllegalPickup, IllegalDelivery, \
    UnsupportedIntention, find_position_after_move, check_for_out_of_bounds_moves, group_intentions_by_item_to_pickup, \
    shuffle_grouped_pickup_intentions, enact_move_intention
from src.utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('TopCongestionEnvironmentLogger', 'top_congestion_environment.log')


def get_item_index_by_id(items_list, item_id):
    # Find the index of the item with the matching id
    item_index = next((index for index, item in enumerate(items_list) if item.id == item_id), None)

    # If an item with the matching id is found, return its index
    if item_index is not None:
        return item_index

    # If no item with the matching id is found, return None
    return None

def check_for_collisions_with_obstacles(intentions: list[Intention], state: Grid) -> None:
    move_intentions = filter(lambda intention: isinstance(intention, Move), intentions)

    for move_intention in move_intentions:
        new_x, new_y = find_position_after_move(move_intention, state)
        # Check if the new position is occupied by an obstacle
        if any((isinstance(board_object, Obstacle) for board_object in state.board[new_x][new_y])):
            raise IllegalMove(f"Agent {move_intention.agent_id} tried to move into an {state.board[new_x][new_y]} "
                              f"in position {(new_x, new_y)}")


def check_for_pickups_from_outside_station(intentions: list[Intention], state: Grid) -> None:
    pickup_intentions = filter(lambda intention: isinstance(intention, Pickup), intentions)

    for pickup_intention in pickup_intentions:
        agent_index = state.get_agent_index_by_id(pickup_intention.agent_id)
        agent_position = state.agents[agent_index].position
        x, y = agent_position
        # Check if the agent is on a pickup station
        if not any((isinstance(board_object, PickupStation) for board_object in state.board[x][y])):
            raise IllegalPickup(f"Agent {pickup_intention.agent_id} tried to pick up an item from a non-pickup station")


def check_for_deliveries_from_outside_station(intentions: list[Intention], state: Grid) -> None:
    deliver_intentions = filter(lambda intention: isinstance(intention, Deliver), intentions)

    for deliver_intention in deliver_intentions:
        agent_index = state.get_agent_index_by_id(deliver_intention.agent_id)
        agent_position = state.agents[agent_index].position
        x, y = agent_position
        # Check if the agent is on a delivery station
        if not any((isinstance(board_object, DeliveryStation) for board_object in state.board[x][y])):
            raise IllegalDelivery(f"Agent {deliver_intention.agent_id} tried to deliver an item to a non-delivery "
                                  f"station")


def check_if_intentions_come_from_unique_agents(intentions: list[Intention]) -> None:
    unique_sources = {intention.agent_id for intention in intentions}
    if len(unique_sources) < len(intentions):
        raise IllegalIntention("Multiple intentions came from the same agent")


def conflicts_for_same_item(grouped_intentions: dict[int, dict[int, list[Pickup]]]) -> list[Pickup]:
    """Find all intentions that are trying to pick up the same item"""
    conflicting_intentions = []

    for pickup_station_id, item_intentions in grouped_intentions.items():
        for item_id, intentions in item_intentions.items():
            # None means that the agent wants to pick up any item. This is not a conflict.
            if len(intentions) > 1 and item_id is not None:
                conflicting_intentions.extend(intentions[1:])

    return conflicting_intentions


def overflowing_pickups(grouped_intentions: dict[int, dict[int | None, list[Pickup]]], state: Grid) -> list[Pickup]:
    """Find intentions to pick up any item that won't be served, as there are not enough items in the pickup station
    (giving away concrete items had priority)"""
    overflow_intentions = []

    for pickup_station_id, item_intentions in grouped_intentions.items():
        # We only calculate 1 request per concrete item, as conflicting ones were rejected in the other step
        number_of_concrete_item_requests = len(item_intentions.keys()) if None not in item_intentions.keys() \
            else len(item_intentions.keys()) - 1
        pickup_station_index = state.get_pickup_station_index_by_id(pickup_station_id)
        number_of_awaiting_items = len(state.pickup_stations[pickup_station_index].items)
        number_of_freely_available_items = number_of_awaiting_items - number_of_concrete_item_requests

        if len(item_intentions[None]) > number_of_freely_available_items:
            overflow_intentions.extend(item_intentions[None][number_of_freely_available_items:])

    return overflow_intentions


def _enact_deliver_intention(deliver_intention: Deliver, state: Grid, tick: int) -> Grid:
    # Find the item in the agent's inventory
    agent_index = state.get_agent_index_by_id(deliver_intention.agent_id)
    agent = state.agents[agent_index]
    try:
        item_to_deliver = next((item for item in agent.items if item.status is ItemStatus.IN_TRANSIT))
    except StopIteration:
        raise IllegalDelivery(f"Agent {deliver_intention.agent_id} tried to deliver an item that it does not have")

    # Change the item's status. It is not actually dropped to the delivery station.
    item_to_deliver.set_status(ItemStatus.DELIVERED, tick)
    logger.info(f"Item {item_to_deliver} delivered by agent {deliver_intention.agent_id}")
    print(f"Item {item_to_deliver} delivered by agent {deliver_intention.agent_id}")

    return state


def _enact_pickup_intention(pickup_intention: Pickup, state: Grid, tick: int) -> Grid:
    # Find the agent's location and the pickup station
    agent_index = state.get_agent_index_by_id(pickup_intention.agent_id)
    agent_position = state.agents[agent_index].position
    pickup_station = next((board_object for board_object in
                           state.board[agent_position[0]][agent_position[1]]
                           if isinstance(board_object, PickupStation)))
    # Get item index in pickup station
    item_index = get_item_index_by_id(pickup_station.items, pickup_intention.item_id)
    try:
        item = pickup_station.items.pop(item_index)
    except IndexError:
        raise IllegalPickup(f"Agent {pickup_intention.agent_id} tried to pick up an item that is not in the pickup "
                            f"station")
    item.set_status(ItemStatus.IN_TRANSIT, tick)
    logger.info(f"Item {item} picked up by agent {pickup_intention.agent_id}")
    print(f"Item {item} picked up by agent {pickup_intention.agent_id}")
    agent_index = state.get_agent_index_by_id(pickup_intention.agent_id)
    state.agents[agent_index].items.append(item)

    return state


class TopCongestionEnvironment(Environment):
    def _illegal_intentions(self, intentions: list[Intention], state: Grid) -> None:
        try:
            check_for_out_of_bounds_moves(intentions, state)
            check_for_collisions_with_obstacles(intentions, state)
            check_for_pickups_from_outside_station(intentions, state)
            check_for_deliveries_from_outside_station(intentions, state)
        except Exception as e:
            logger.error(f"Illegal intention detected: {e}")  # log error message
            raise

    def _contradicting_intentions(self, intentions: list[Intention], state: Grid) -> list[Intention]:
        """We don't detect collisions in this Environment, so the only contradicting Intentions are 2 agents trying to
        pick up the same item, be it from the same id or more pickup intentions than items in the pickup station"""
        contradicting_intentions = []
        pickup_intentions = list(filter(lambda intention: isinstance(intention, Pickup), intentions))
        grouped_intentions = group_intentions_by_item_to_pickup(pickup_intentions, state)
        shuffled_grouped_intentions = shuffle_grouped_pickup_intentions(grouped_intentions)

        contradicting_intentions.extend(conflicts_for_same_item(shuffled_grouped_intentions))
        contradicting_intentions.extend(overflowing_pickups(shuffled_grouped_intentions, state))

        return contradicting_intentions

    def _enact_valid_intentions(self, consistent_intentions: list[Intention], state: Grid, tick: int) -> Grid:
        for intention in consistent_intentions:
            if isinstance(intention, Pickup):
                state = _enact_pickup_intention(intention, state, tick)
            elif isinstance(intention, Deliver):
                state = _enact_deliver_intention(intention, state, tick)
            elif isinstance(intention, Move):
                state = enact_move_intention(intention, state)
            else:
                raise UnsupportedIntention(f"Intention {intention} is not supported")

        return state

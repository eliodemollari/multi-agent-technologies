import random

from simulation.base.environment import ItemFactory
from simulation.base.grid import Grid
from simulation.base.item import Item
from simulation.item_factories.common import target_stations_exist, StationDoesNotExist


def _create_items(tick: int, number_of_items: int, source_station_id: int, delivery_weights: dict[int, int]) \
        -> list[Item]:
    targets = list(delivery_weights.keys())
    weights = list(delivery_weights.values())
    destination_list = random.choices(population=targets, weights=weights, k=number_of_items)

    return [Item(tick, source_station_id, destination_station_id) for destination_station_id in destination_list]


class WeightedDistribution(ItemFactory):
    """Strategy that adds items at each step of the simulation according to the predefined distribution. It consists of
    a chance for a pickup station to be chosen at a given step and a number of steps per simulation tick. Delivery
    station is chosen independently for each item by a weighted choice."""

    def __init__(self, pickup_distribution: dict[int, float], delivery_weights: dict[int, int],
                 steps_per_tick: int):
        """:param pickup_distribution: A dictionary of pickup stations to a probability of adding an item to that
        station in a given step.
        :param delivery_weights: A dictionary of delivery stations to a weight of choosing that station as a target for
        a new item.
        :param steps_per_tick: Number of draws per simulation tick. The higher it is, the bigger is the expected number
        of items to add, unless all pickup_distribution values are set to 0."""
        self._pickup_distribution = pickup_distribution
        self._delivery_weights = delivery_weights
        self._steps_per_tick = steps_per_tick
        self._target_stations_checked = False

    def __check_targets_if_needed(self, state: Grid) -> None:
        """Check if target stations passed in delivery weights exist in the grid. If not, raise a StationDoesNotExist
        exception"""
        if not self._target_stations_checked:
            target_stations_exist(set(self._delivery_weights.keys()), state)
            self._target_stations_checked = True

    def add_items(self, state: Grid, tick: int) -> Grid:
        self.__check_targets_if_needed(state)
        for pickup_station_id, probability in self._pickup_distribution.items():
            # Not using random.binomialvariate, since we are not all on Python 3.12 yet
            number_of_items_to_add = sum(random.random() < probability for _ in range(self._steps_per_tick))
            try:
                state.pickup_stations[pickup_station_id].to_collect.extend(
                    _create_items(tick, number_of_items_to_add, pickup_station_id, self._delivery_weights))
            except KeyError as e:
                raise StationDoesNotExist(f"Source station {e} does not exist")

        return state

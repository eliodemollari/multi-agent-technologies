import random
from typing import Iterable

from simulation.base.environment import ItemFactory
from simulation.base.grid import Grid
from simulation.base.item import Item
from simulation.item_factories.common import StationDoesNotExist, target_stations_exist


def _target_stations_exist(targets: Iterable[list[int]], grid: Grid) -> None:
    """Check if target stations passed in initial distribution exist. If not, raise a StationDoesNotExist exception"""
    all_targets_from_distribution = {target_id for target_list in targets for target_id in target_list}
    target_stations_exist(all_targets_from_distribution, grid)


class InitialDistribution(ItemFactory):
    """Strategy that adds a fixed number of items at the start of the simulation"""

    def __init__(self, distribution: dict[int, list[int]] | int):
        """:param distribution: A dictionary of pickup stations to a list of delivery stations, or an integer, which
        will be used as the number of items to add to each pickup station. The delivery stations will be chosen
        randomly from all delivery stations with uniform probability."""
        self._distribution = distribution

    def __simple_distribution(self, state: Grid, tick: int) -> Grid:
        """Adds identical number of items to pickup stations with random destinations"""
        potential_destinations = list(state.delivery_stations.keys())

        for pickup_station_id in state.pickup_stations.keys():
            random_destinations = random.choices(potential_destinations, k=self._distribution)
            state.pickup_stations[pickup_station_id].to_collect = [Item(tick, pickup_station_id, destination_station)
                                                                   for destination_station in random_destinations]

        return state

    def __exact_distribution(self, state: Grid, tick: int) -> Grid:
        """Adds items to each pickup station with sources - keys in the dictionary and destinations - values under
        those keys. The targets will be added in the same order they are placed in the list."""
        _target_stations_exist(self._distribution.values(), state)

        for (source_station, targets) in self._distribution.items():
            try:
                state.pickup_stations[source_station].to_collect = \
                    [Item(tick, source_station, destination_station) for destination_station in targets]
            except KeyError as e:
                raise StationDoesNotExist(f"Source station {e} does not exist")

        return state

    def add_items(self, state: Grid, tick: int) -> Grid:
        if tick == 0:
            if isinstance(self._distribution, int):
                return self.__simple_distribution(state, tick)
            else:
                return self.__exact_distribution(state, tick)

        return state

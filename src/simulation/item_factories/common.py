from src.simulation.base.grid import Grid


class StationDoesNotExist(Exception):
    pass


def target_stations_exist(targets: set[int], grid: Grid) -> None:
    """For a set of target station identifiers, check if they exist in the grid. If not, raise a StationDoesNotExist
    exception"""
    non_existent_targets = targets.difference(grid.delivery_stations.keys())

    if len(non_existent_targets) > 0:
        raise StationDoesNotExist(f"Target stations {non_existent_targets} do not exist")

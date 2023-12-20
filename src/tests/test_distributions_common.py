from simulation.base.grid import Grid, PickupStation, DeliveryStation


def setup_grid() -> Grid:
    """Create Grid with pickup stations: 1, and 32, and delivery stations: 1, 2, 3, "a", "b", "c", no agents,
    and no obstacles. Board may be empty for the purpose of testing ItemFactory"""
    pickup_stations = {
        1: PickupStation(),
        2: PickupStation()
    }
    delivery_stations = {
        1: DeliveryStation(),
        2: DeliveryStation(),
        3: DeliveryStation(),
        "a": DeliveryStation(),
        "b": DeliveryStation(),
        "c": DeliveryStation()
    }
    agents = {}
    board = [[]]
    return Grid(pickup_stations, delivery_stations, agents, board)

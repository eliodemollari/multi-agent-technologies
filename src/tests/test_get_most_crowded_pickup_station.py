import unittest
from src.simulation.base.grid import Grid, PickupStation, DeliveryStation
from src.simulation.base.item import Item, ItemStatus


class TestGrid(unittest.TestCase):
    def setUp(self):
        # Create grid
        self.grid = Grid([[[] for _ in range(10)] for _ in range(10)])

        # Create pickup stations
        self.pickup_station1 = PickupStation(position=(1, 1))
        self.pickup_station2 = PickupStation(position=(2, 2))
        self.pickup_station3 = PickupStation(position=(3, 3))

        # Add pickup stations to grid
        self.grid.add_board_object(self.pickup_station1)
        self.grid.add_board_object(self.pickup_station2)
        self.grid.add_board_object(self.pickup_station3)

        # Create delivery stations
        self.delivery_station1 = DeliveryStation(position=(4, 4))
        self.delivery_station2 = DeliveryStation(position=(5, 5))
        self.delivery_station3 = DeliveryStation(position=(6, 6))

        # Add delivery stations to grid
        self.grid.add_board_object(self.delivery_station1)
        self.grid.add_board_object(self.delivery_station2)
        self.grid.add_board_object(self.delivery_station3)

        # Add items to pickup stations
        for _ in range(5):
            self.pickup_station1.items.append(Item(status=ItemStatus.AWAITING_PICKUP, created_tick=0, source=self.pickup_station1, destination=self.delivery_station1))
        for _ in range(3):
            self.pickup_station2.items.append(Item(status=ItemStatus.AWAITING_PICKUP, created_tick=0, source=self.pickup_station2, destination=self.delivery_station2))
        for _ in range(7):
            self.pickup_station3.items.append(Item(status=ItemStatus.AWAITING_PICKUP, created_tick=0, source=self.pickup_station3, destination=self.delivery_station3))

    def test_get_most_crowded_pickup_stations(self):
        most_crowded_station = self.grid.get_most_crowded_pickup_station()
        self.assertEqual(self.pickup_station3, most_crowded_station)


if __name__ == '__main__':
    unittest.main()

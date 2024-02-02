import unittest

from src.simulation.base.grid import Grid, PickupStation, DeliveryStation, Obstacle
from src.simulation.base.item import Item, ItemStatus
from src.simulation.reactive_agents import TopCongestionAgent


class TestMakeBid(unittest.TestCase):
    def test_make_bid(self):
        self.board = [[[] for _ in range(11)] for _ in range(11)]
        grid_size = [11, 11]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent1 = TopCongestionAgent((10, 0), 1)
        self.agent2 = TopCongestionAgent((4, 8), 2)
        self.agent3 = TopCongestionAgent((8, 10), 3)

        self.obstacle1 = Obstacle((5, 0))
        self.obstacle2 = Obstacle((5, 1))

        self.pickup_stations = [
            PickupStation(position=(0, 0)),
            PickupStation(position=(5, 5)),
            PickupStation(position=(10, 7))
        ]
        self.delivery_stations = [
            DeliveryStation(position=(10, 10)),
            DeliveryStation(position=(9, 9))
        ]

        # Set up the first pickup station
        self.item1 = Item(0, self.pickup_stations[0], self.delivery_stations[0], ItemStatus.AWAITING_PICKUP)
        # self.item2 = Item(0, self.pickup_stations[0], self.delivery_stations[1], ItemStatus.AWAITING_PICKUP)
        # self.item3 = Item(0, self.pickup_stations[0], self.delivery_stations[0], ItemStatus.AWAITING_PICKUP)
        self.pickup_stations[0].items.append(self.item1)
        # self.pickup_stations[0].items.append(self.item2)
        # self.pickup_stations[0].items.append(self.item3)

        # Set up the second pickup station
        self.item4 = Item(0, self.pickup_stations[1], self.delivery_stations[0], ItemStatus.AWAITING_PICKUP)
        # self.item5 = Item(0, self.pickup_stations[1], self.delivery_stations[1], ItemStatus.AWAITING_PICKUP)
        # self.item6 = Item(0, self.pickup_stations[1], self.delivery_stations[0], ItemStatus.AWAITING_PICKUP)
        self.pickup_stations[1].items.append(self.item4)
        # self.pickup_stations[1].items.append(self.item5)
        # self.pickup_stations[1].items.append(self.item6)

        # Set up the third pickup station
        self.item7 = Item(0, self.pickup_stations[2], self.delivery_stations[0], ItemStatus.AWAITING_PICKUP)
        # self.item8 = Item(0, self.pickup_stations[2], self.delivery_stations[1], ItemStatus.AWAITING_PICKUP)
        # self.item9 = Item(0, self.pickup_stations[2], self.delivery_stations[0], ItemStatus.AWAITING_PICKUP)
        self.pickup_stations[2].items.append(self.item7)
        # self.pickup_stations[2].items.append(self.item8)
        # self.pickup_stations[2].items.append(self.item9)

        self.grid.add_board_object(self.agent1)
        self.grid.add_board_object(self.agent2)
        self.grid.add_board_object(self.agent3)
        self.grid.add_board_object(self.obstacle1)
        self.grid.add_board_object(self.obstacle2)
        self.grid.add_board_object(self.pickup_stations[0])
        self.grid.add_board_object(self.pickup_stations[1])
        self.grid.add_board_object(self.pickup_stations[2])
        self.grid.add_board_object(self.delivery_stations[0])
        self.grid.add_board_object(self.delivery_stations[1])

        all_items = [item for station in self.grid.pickup_stations for item in station.items if item.status == ItemStatus.AWAITING_PICKUP]

        # Get all possible bundles
        agent1_bundles = self.agent1.receive_auction_information(all_items, self.grid)
        agent2_bundles = self.agent2.receive_auction_information(all_items, self.grid)
        agent3_bundles = self.agent3.receive_auction_information(all_items, self.grid)

        self.assertEqual(len(agent1_bundles), 3)
        self.assertEqual(len(agent2_bundles), 6)
        self.assertEqual(len(agent3_bundles), 7)





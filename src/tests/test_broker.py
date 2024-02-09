import unittest
from src.simulation.base.grid import Grid, Obstacle
from src.simulation.environments.broker import Broker
from src.simulation.base.item import Item, ItemStatus
from src.simulation.base.grid import PickupStation, DeliveryStation
from src.simulation.reactive_agents import TopCongestionAgent


class TestBroker(unittest.TestCase):

    def test_announce_items(self):
        self.board = [[[] for _ in range(10)] for _ in range(10)]
        grid_size = [10, 10]
        self.grid = Grid(self.board, grid_size)

        self.agent1 = TopCongestionAgent((9, 0), 2)
        self.agent2 = TopCongestionAgent((4, 8), 2)
        self.agent3 = TopCongestionAgent((8, 9), 2)

        self.obstacle1 = Obstacle((5, 0))
        self.obstacle2 = Obstacle((5, 1))

        self.pickup_stations = [
            PickupStation(position=(0, 0)),
            PickupStation(position=(4, 4)),
            PickupStation(position=(9, 7))
        ]
        self.delivery_stations = [
            DeliveryStation(position=(8, 8)),
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

        broker = Broker(self.grid)

        broker.assign_items_to_agents()

        self.assertEqual(self.item4.agent_id, self.agent2.id)
        self.assertEqual(self.item1.agent_id, self.agent2.id)
        self.assertEqual(self.item7.agent_id, self.agent3.id)

        self.assertEqual(self.agent1.total_cost, 17)
        self.assertEqual(self.agent3.total_cost, 3)

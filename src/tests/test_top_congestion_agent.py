import unittest

from simulation.base.grid import Grid, PickupStation, DeliveryStation, Item
from simulation.base.intentions import Move, Pickup, Deliver
from simulation.base.item import ItemStatus
from simulation.reactive_agents import TopCongestionAgent
from tests.test_grid import sample_empty_3x3_board


class TestTopCongestionAgent(unittest.TestCase):
    def setUp(self):
        # setup method to initialize common test objects
        self.agent = TopCongestionAgent()
        self.board = sample_empty_3x3_board()
        self.grid = Grid({}, {}, {0: self.agent}, self.board)

    def test_agent_carrying_item(self):
        # Test scenario where agent is carrying an item
        item = Item(0, 0, 0, status=ItemStatus.IN_TRANSIT)
        self.agent.items.append(item)
        self.grid.delivery_stations = {0: DeliveryStation()}

        # Agent is on the DeliveryStation
        self.grid.add_board_object(self.agent, (0, 0))
        self.grid.add_board_object(self.grid.delivery_stations[0], (0, 0))

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Deliver)

    def test_agent_not_carrying_item_on_pickup_station(self):
        # Test scenario where agent is not carrying an item and is on a PickupStation
        pickup_station = PickupStation([Item(0, 0, 0) for _ in range(5)])
        self.grid.pickup_stations = {0: pickup_station}
        self.grid.add_board_object(pickup_station, (0, 0))
        self.grid.add_board_object(self.agent, (0, 0))

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Pickup)

    def test_agent_not_carrying_item_not_on_pickup_station(self):
        # Test scenario where agent is not carrying an item and is not on a PickupStation
        pickup_station = PickupStation([Item(0, 0, 0) for _ in range(5)])
        self.grid.pickup_stations = {0: pickup_station}
        self.grid.add_board_object(pickup_station, (1, 1))
        self.grid.add_board_object(self.agent, (0, 0))

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Move)

    # Additional tests can be added for different scenarios


if __name__ == '__main__':
    unittest.main()

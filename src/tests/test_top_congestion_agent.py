import unittest

from src.simulation.base.grid import Grid, PickupStation, DeliveryStation, Obstacle
from src.simulation.base.intentions import Move, Pickup
from src.simulation.base.item import ItemStatus, Item
from src.simulation.reactive_agents import TopCongestionAgent


class TestTopCongestionAgent(unittest.TestCase):
    def setUp(self):
        self.board = [[[] for _ in range(10)] for _ in range(10)]
        grid_size = [10, 10]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent = TopCongestionAgent((0, 0))
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station = DeliveryStation(position=(2, 2))
        self.obstacle = Obstacle(position=(3, 3))

        self.grid.add_board_object(self.agent)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station)
        self.grid.add_board_object(self.obstacle)

    def test_agent_carrying_item(self):
        # Test scenario where agent is carrying an item
        item = Item(0, self.pickup_station, self.delivery_station, ItemStatus.IN_TRANSIT)
        self.agent.items.append(item)

        self.assertEqual(self.agent.is_carrying_item, True)

    def test_agent_not_carrying_item_on_pickup_station(self):
        # Test scenario where agent is not carrying an item and is on a PickupStation
        # Add items to pickup stations
        for _ in range(5):
            self.pickup_station.items.append(
                Item(
                    status=ItemStatus.AWAITING_PICKUP,
                    created_tick=0,
                    source=self.pickup_station,
                    destination=self.delivery_station
                )
            )

        # Agent on pickup station
        self.pickup_station.set_position((0, 0))

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Pickup)

    def test_agent_not_carrying_item_not_on_pickup_station(self):
        # Test scenario where agent is not carrying an item and is not on a PickupStation
        # Add items to pickup stations
        for _ in range(5):
            self.pickup_station.items.append(
                Item(status=ItemStatus.AWAITING_PICKUP,
                     created_tick=0,
                     source=self.pickup_station,
                     destination=self.delivery_station
                     )
            )

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Move)

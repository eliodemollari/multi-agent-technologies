import unittest

from src.simulation.base.grid import Grid, PickupStation, DeliveryStation, Obstacle
from src.simulation.base.intentions import Move, Pickup, Deliver
from src.simulation.base.item import ItemStatus, Item
from src.simulation.reactive_agents import TopCongestionAgent


class TestTopCongestionAgent(unittest.TestCase):
    def setUp(self):
        self.board = [[[] for _ in range(10)] for _ in range(10)]
        grid_size = [10, 10]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent = TopCongestionAgent((0, 0), 3)
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station1 = DeliveryStation(position=(7, 7))
        self.delivery_station2 = DeliveryStation(position=(8, 8))
        self.obstacle = Obstacle(position=(4, 4))

        self.grid.add_board_object(self.agent)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station1)
        self.grid.add_board_object(self.delivery_station2)
        self.grid.add_board_object(self.obstacle)

    def test_agent_carrying_item(self):
        # Test scenario where agent is carrying an item
        item1 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.IN_TRANSIT)
        item2 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.IN_TRANSIT)
        self.agent.items.append(item1)
        self.agent.items.append(item2)

        self.assertEqual(len(self.agent.get_carried_items()), 2)

    def test_agent_having_all_items_in_transit(self):
        """
        Test scenario where agent has all items in transit
        The agent should move to the delivery station of the item with the highest priority
        :return: Move intention
        """
        item1 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.IN_TRANSIT, 1)
        item2 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.IN_TRANSIT, 2)
        item3 = Item(0, self.pickup_station, self.delivery_station2, ItemStatus.IN_TRANSIT, 3)

        self.agent.items.append(item1)
        self.agent.items.append(item2)
        self.agent.items.append(item3)

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Move)

    def test_agent_having_all_items_in_transit_on_delivery_station(self):
        """
        Test scenario where agent has all items in transit
        And the agent is on the delivery station of the item with the highest priority
        :return: Move intention
        """
        item1 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.IN_TRANSIT, 1)
        item2 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.IN_TRANSIT, 2)
        item3 = Item(0, self.pickup_station, self.delivery_station2, ItemStatus.IN_TRANSIT, 3)

        self.agent.items.append(item1)
        self.agent.items.append(item2)
        self.agent.items.append(item3)

        # Agent on delivery station
        self.agent.set_position(self.delivery_station1.position)

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Deliver)

    def test_agent_having_assigned_items_to_pickup(self):
        """
        Test scenario where agent has assigned items to pickup
        And the agent is not on the pickup station of the assigned item with the highest priority
        :return: Move intention
        """
        item1 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.ASSIGNED_TO_AGENT, 1)
        item2 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.ASSIGNED_TO_AGENT, 2)
        item3 = Item(0, self.pickup_station, self.delivery_station2, ItemStatus.ASSIGNED_TO_AGENT, 3)

        self.agent.items.append(item1)
        self.agent.items.append(item2)
        self.agent.items.append(item3)

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Move)

    def test_agent_having_assigned_items_to_pickup_on_pickup_station(self):
        """
        Test scenario where agent has assigned items to pickup
        And the agent is on the pickup station of the assigned item with the highest priority
        :return: Pickup intention
        """
        item1 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.ASSIGNED_TO_AGENT, 1)
        item2 = Item(0, self.pickup_station, self.delivery_station1, ItemStatus.ASSIGNED_TO_AGENT, 2)
        item3 = Item(0, self.pickup_station, self.delivery_station2, ItemStatus.ASSIGNED_TO_AGENT, 3)

        self.agent.items.append(item1)
        self.agent.items.append(item2)
        self.agent.items.append(item3)

        # Agent on pickup station
        self.agent.set_position(self.pickup_station.position)

        intention = self.agent.make_intention(self.grid)
        self.assertIsInstance(intention, Pickup)

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

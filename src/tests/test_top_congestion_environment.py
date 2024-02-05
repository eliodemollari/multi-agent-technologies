import unittest

from src.simulation.base.grid import Grid, Obstacle, PickupStation, DeliveryStation
from src.simulation.base.intentions import Move, Pickup, Deliver
from src.simulation.base.item import Item, ItemStatus
from src.simulation.environments.common import IllegalMove, IllegalPickup, IllegalIntention, \
    group_intentions_by_item_to_pickup, IllegalDelivery
from src.simulation.environments.top_congestion_environment import check_for_collisions_with_obstacles, \
    check_for_pickups_from_outside_station, check_for_deliveries_from_outside_station, \
    check_if_intentions_come_from_unique_agents, conflicts_for_same_item, _enact_pickup_intention
from src.simulation.reactive_agents import TopCongestionAgent


class TestTopCongestionEnvironment(unittest.TestCase):
    def test_check_for_collisions_with_obstacles(self):
        self.board = [[[] for _ in range(11)] for _ in range(11)]
        grid_size = [11, 11]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent = TopCongestionAgent((2, 3))
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station = DeliveryStation(position=(2, 2))
        self.obstacle = Obstacle(position=(3, 3))

        self.grid.add_board_object(self.agent)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station)
        self.grid.add_board_object(self.obstacle)

        """Test that check_for_collisions_with_obstacles raises an exception when an agent tries to move into
        an obstacle"""

        move_intention = Move(self.agent.id, Move.RIGHT)

        with self.assertRaises(IllegalMove):
            check_for_collisions_with_obstacles([move_intention], self.grid)

    def test_check_for_pickups_from_outside_station(self):
        self.board = [[[] for _ in range(11)] for _ in range(11)]
        grid_size = [11, 11]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent = TopCongestionAgent((1, 0))
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station = DeliveryStation(position=(2, 2))
        self.item = Item(0, self.pickup_station, self.delivery_station, ItemStatus.AWAITING_PICKUP)
        self.pickup_station.items.append(self.item)
        self.obstacle = Obstacle(position=(3, 3))

        self.grid.add_board_object(self.agent)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station)
        self.grid.add_board_object(self.obstacle)

        illegal_intention = [Pickup(self.agent.id, self.item.id)]

        with self.assertRaises(IllegalPickup):
            check_for_pickups_from_outside_station(illegal_intention, self.grid)

    def test_check_for_deliveries_from_outside_station(self):
        self.board = [[[] for _ in range(11)] for _ in range(11)]
        grid_size = [11, 11]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent = TopCongestionAgent((1, 0))
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station = DeliveryStation(position=(2, 2))
        self.item = Item(2, self.pickup_station, self.delivery_station, ItemStatus.IN_TRANSIT)
        self.agent.items.append(self.item)
        self.obstacle = Obstacle(position=(3, 3))

        self.grid.add_board_object(self.agent)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station)
        self.grid.add_board_object(self.obstacle)

        illegal_intention = [Deliver(self.agent.id, self.item.id)]

        with self.assertRaises(IllegalDelivery):
            check_for_deliveries_from_outside_station(illegal_intention, self.grid)

    def test_check_if_intentions_come_from_unique_agents(self):
        self.board = [[[] for _ in range(11)] for _ in range(11)]
        grid_size = [11, 11]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent = TopCongestionAgent((1, 0))
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station = DeliveryStation(position=(2, 2))
        self.item = Item(0, self.pickup_station, self.delivery_station, ItemStatus.AWAITING_PICKUP)
        self.pickup_station.items.append(self.item)
        self.obstacle = Obstacle(position=(3, 3))

        self.grid.add_board_object(self.agent)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station)
        self.grid.add_board_object(self.obstacle)

        illegal_intentions = [
            Pickup(self.agent.id, self.item.id),
            Pickup(self.agent.id, self.item.id)
        ]

        with self.assertRaises(IllegalIntention):
            check_if_intentions_come_from_unique_agents(illegal_intentions)

    def test_conflicts_for_same_item(self):
        self.board = [[[] for _ in range(11)] for _ in range(11)]
        grid_size = [11, 11]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent_1 = TopCongestionAgent((1, 1))
        self.agent_2 = TopCongestionAgent((1, 1))
        self.agent_3 = TopCongestionAgent((1, 1))
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station = DeliveryStation(position=(2, 2))
        self.item_1 = Item(0, self.pickup_station, self.delivery_station, ItemStatus.AWAITING_PICKUP)
        self.item_2 = Item(0, self.pickup_station, self.delivery_station, ItemStatus.AWAITING_PICKUP)
        self.pickup_station.items.append(self.item_1)
        self.pickup_station.items.append(self.item_2)
        self.obstacle = Obstacle(position=(3, 3))

        self.grid.add_board_object(self.agent_1)
        self.grid.add_board_object(self.agent_2)
        self.grid.add_board_object(self.agent_3)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station)
        self.grid.add_board_object(self.obstacle)

        conflicting_intentions = [
            Pickup(self.agent_1.id, self.item_1.id),
            Pickup(self.agent_2.id, self.item_1.id)
        ]
        non_conflicting_intention = Pickup(self.agent_3.id, self.item_2.id)
        all_intentions = conflicting_intentions + [non_conflicting_intention]
        grouped_intentions = group_intentions_by_item_to_pickup(all_intentions, self.grid)
        found_conflicts = conflicts_for_same_item(grouped_intentions)

        self.assertEqual(len(found_conflicts), 1)
        self.assertIn(found_conflicts[0], conflicting_intentions)
        self.assertNotIn(found_conflicts[0], [non_conflicting_intention])

    def test_enact_pickup_intention(self):
        """Test that enact_pickup_intention picks up the item"""
        self.board = [[[] for _ in range(11)] for _ in range(11)]
        grid_size = [11, 11]
        self.grid = Grid(self.board, grid_size)

        # Create objects on the grid
        self.agent = TopCongestionAgent((1, 1))
        self.pickup_station = PickupStation(position=(1, 1))
        self.delivery_station = DeliveryStation(position=(2, 2))
        self.item = Item(0, self.pickup_station, self.delivery_station, ItemStatus.AWAITING_PICKUP)
        self.pickup_station.items.append(self.item)
        self.obstacle = Obstacle(position=(3, 3))

        self.grid.add_board_object(self.agent)
        self.grid.add_board_object(self.pickup_station)
        self.grid.add_board_object(self.delivery_station)
        self.grid.add_board_object(self.obstacle)

        pickup_intention = Pickup(0, self.item.id)

        _enact_pickup_intention(pickup_intention, self.grid)
        self.assertEqual(len(self.pickup_station.items), 0)
        self.assertEqual(self.agent.items, [self.item])
        self.assertEqual(self.agent.items[0].status, ItemStatus.IN_TRANSIT)

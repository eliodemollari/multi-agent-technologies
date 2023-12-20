import unittest

from simulation.base.grid import Grid, Obstacle, PickupStation
from simulation.base.intentions import Move, Pickup, Deliver
from simulation.base.item import Item, ItemStatus
from simulation.environments.common import IllegalMove, IllegalPickup, IllegalIntention, \
    group_intentions_by_item_to_pickup, IllegalDelivery
from simulation.environments.top_congestion_environment import check_for_collisions_with_obstacles, \
    check_for_pickups_from_outside_station, check_for_deliveries_from_outside_station, \
    check_if_intentions_come_from_unique_agents, conflicts_for_same_item, overflowing_pickups, _enact_pickup_intention, \
    TopCongestionEnvironment
from tests.test_display_grid import TestAgent
from tests.test_environment_common import simple_conflict_scenario
from tests.test_grid import sample_empty_3x3_board


class TestTopCongestionEnvironment(unittest.TestCase):
    def test_check_for_collisions_with_obstacles(self):
        """Test that check_for_collisions_with_obstacles raises an exception when an agent tries to move into
        an obstacle"""
        agents = {0: TestAgent()}
        move_intention = Move(0, (1, 1))
        board = sample_empty_3x3_board()
        grid = Grid({}, {}, agents, board)
        grid.add_board_object(agents[0], (0, 0))
        grid.add_board_object(Obstacle(), (1, 1))

        with self.assertRaises(IllegalMove):
            check_for_collisions_with_obstacles([move_intention], grid)

    def test_check_for_pickups_from_outside_station(self):
        agents = {0: TestAgent()}
        board = sample_empty_3x3_board()
        grid = Grid({}, {}, agents, board)
        grid.add_board_object(agents[0], (0, 0))
        illegal_intention = [Pickup(0, 0)]

        with self.assertRaises(IllegalPickup):
            check_for_pickups_from_outside_station(illegal_intention, grid)

    def test_check_for_deliveries_from_outside_station(self):
        agents = {0: TestAgent()}
        board = sample_empty_3x3_board()
        grid = Grid({}, {}, agents, board)
        grid.add_board_object(agents[0], (0, 0))
        illegal_intention = [Deliver(0)]

        with self.assertRaises(IllegalDelivery):
            check_for_deliveries_from_outside_station(illegal_intention, grid)

    def test_check_if_intentions_come_from_unique_agents(self):
        agents = {0: TestAgent()}
        board = sample_empty_3x3_board()
        grid = Grid({}, {}, agents, board)
        illegal_intentions = [Pickup(0, 0), Pickup(0, 0)]
        with self.assertRaises(IllegalIntention):
            check_if_intentions_come_from_unique_agents(illegal_intentions)

    def test_conflicts_for_same_item(self):
        grid = simple_conflict_scenario()
        conflicting_intentions = [Pickup(0, 0), Pickup(1, 0)]
        non_conflicting_intention = Pickup(2, None)
        all_intentions = conflicting_intentions + [non_conflicting_intention]
        grouped_intentions = group_intentions_by_item_to_pickup(all_intentions, grid)
        found_conflicts = conflicts_for_same_item(grouped_intentions)

        self.assertEqual(len(found_conflicts), 1)
        self.assertIn(found_conflicts[0], conflicting_intentions)
        self.assertNotIn(found_conflicts[0], [non_conflicting_intention])

    def test_overflowing_pickups(self):
        grid = simple_conflict_scenario()
        non_overflowing_intentions = [Pickup(0, 0), Pickup(2, None), Pickup(1, 0)]
        overflowing_intentions = [Pickup(3, None), Pickup(4, None), Pickup(5, 0)]
        all_intentions = non_overflowing_intentions + overflowing_intentions
        grouped_intentions = group_intentions_by_item_to_pickup(all_intentions, grid)
        overflowed_intentions = overflowing_pickups(grouped_intentions, grid)

        # Confirm that 2 intentions overflowed, and they came from overflowing_intentions, but not from
        # non_overflowing_intentions
        self.assertEqual(len(overflowed_intentions), 2)
        self.assertIn(overflowed_intentions[0], overflowing_intentions)
        self.assertIn(overflowed_intentions[1], overflowing_intentions)
        self.assertNotIn(overflowed_intentions[0], non_overflowing_intentions)
        self.assertNotIn(overflowed_intentions[1], non_overflowing_intentions)

    def test_enact_pickup_intention(self):
        """Test that enact_pickup_intention picks up the item"""
        item = Item(0, 0, 0)
        agents = {0: TestAgent()}
        pickup_stations = {0: PickupStation([item])}
        pickup_intention = Pickup(0, 0)
        board = sample_empty_3x3_board()
        grid = Grid(pickup_stations, {}, agents, board)
        grid.add_board_object(agents[0], (0, 0))
        grid.add_board_object(pickup_stations[0], (0, 0))
        new_grid = _enact_pickup_intention(pickup_intention, grid)
        self.assertEqual(len(pickup_stations[0].to_collect), 0)
        self.assertEqual(agents[0].items, [item])
        self.assertEqual(agents[0].items[0].status, ItemStatus.IN_TRANSIT)

    def test_contradicting_intentions(self):
        grid = simple_conflict_scenario()
        non_contradicting_intentions = [Pickup(0, 0), Pickup(2, None), Pickup(1, 0)]
        contradicting_intentions = [Pickup(3, None), Pickup(4, None), Pickup(5, 0)]
        all_intentions = non_contradicting_intentions + contradicting_intentions
        top_congestion_environment = TopCongestionEnvironment(None, grid)
        found_contradicting_intentions = top_congestion_environment._contradicting_intentions(all_intentions, grid)

        self.assertEqual(len(found_contradicting_intentions), 3)
        self.assertIn(contradicting_intentions[0], found_contradicting_intentions)
        self.assertIn(contradicting_intentions[1], found_contradicting_intentions)
        self.assertNotIn(contradicting_intentions[0], non_contradicting_intentions)
        self.assertNotIn(contradicting_intentions[1], non_contradicting_intentions)

import unittest

from simulation.base.grid import Grid, PickupStation
from simulation.base.intentions import Move, Pickup
from simulation.base.item import Item
from simulation.environments.common import find_position_after_move, check_for_out_of_bounds_moves, IllegalMove, \
    enact_move_intention, group_intentions_by_item_to_pickup
from tests.test_display_grid import TestAgent
from tests.test_grid import sample_empty_3x3_board


def simple_conflict_scenario() -> Grid:
    agents = {0: TestAgent(), 1: TestAgent(), 2: TestAgent(), 3: TestAgent(), 4: TestAgent(), 5: TestAgent()}
    # Create 3 pickup stations
    pickup_stations = {0: PickupStation([Item(0, 0, 0) for _ in range(5)]),
                       1: PickupStation([Item(1, 0, 0) for _ in range(5)]),
                       "a": PickupStation([Item(1, 0, 0)])}

    # Create a 3x3 board, where 2 agents will be at location of pickup_station 0, and 1 agent at location of
    # pickup_station 1
    board = sample_empty_3x3_board()
    grid = Grid(pickup_stations, {}, agents, board)
    grid.add_board_object(pickup_stations[0], (0, 0))
    grid.add_board_object(agents[0], (0, 0))
    grid.add_board_object(agents[1], (0, 0))
    grid.add_board_object(pickup_stations[1], (1, 1))
    grid.add_board_object(agents[2], (1, 1))
    grid.add_board_object(pickup_stations["a"], (2, 2))
    grid.add_board_object(agents[3], (2, 2))
    grid.add_board_object(agents[4], (2, 2))
    grid.add_board_object(agents[5], (2, 2))

    return grid


class TestEnvironmentCommon(unittest.TestCase):
    def test_find_position_after_move(self):
        """Test that find_position_after_move returns the correct position after a move"""
        agents = {0: TestAgent()}
        move_intention = Move(0, (1, 1))
        board = sample_empty_3x3_board()
        grid = Grid({}, {}, agents, board)
        grid.add_board_object(agents[0], (0, 0))
        position = find_position_after_move(move_intention, grid)
        self.assertEqual(position, (1, 1))

    def test_check_for_out_of_bound_moves(self):
        """Test that check_for_out_of_bounds_moves raises an exception when an agent tries to move out of bounds"""
        agents = {0: TestAgent()}
        move_intention = Move(0, (1, 1))
        board = sample_empty_3x3_board()
        grid = Grid({}, {}, agents, board)
        grid.add_board_object(agents[0], (2, 2))
        with self.assertRaises(IllegalMove):
            check_for_out_of_bounds_moves([move_intention], grid)

    def test_enact_move_intention(self):
        """Test that enact_move_intention moves the agent to the correct position"""
        agents = {0: TestAgent()}
        move_intention = Move(0, (1, 1))
        board = sample_empty_3x3_board()
        grid = Grid({}, {}, agents, board)
        grid.add_board_object(agents[0], (0, 0))
        new_grid = enact_move_intention(move_intention, grid)
        self.assertEqual(new_grid.agents[0], agents[0])
        self.assertEqual(new_grid.board[0][0], [])
        self.assertEqual(new_grid.board[1][1], [agents[0]])

    def test_group_intentions_by_item_to_pickup(self):
        grid = simple_conflict_scenario()

        # Create a list of overlapping pickup intentions
        pickup_intentions = [Pickup(0, 0), Pickup(2, None), Pickup(1, 0)]

        grouped_intentions = group_intentions_by_item_to_pickup(pickup_intentions, grid)
        self.assertEqual(len(grouped_intentions.keys()), 2)
        self.assertEqual(list(grouped_intentions[0].keys()), [0])
        self.assertEqual(list(grouped_intentions[1].keys()), [None])
        self.assertEqual(len(grouped_intentions[0][0]), 2)
        self.assertEqual(len(grouped_intentions[1][None]), 1)

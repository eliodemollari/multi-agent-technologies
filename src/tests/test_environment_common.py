import unittest

from src.simulation.base.grid import Grid, PickupStation, DeliveryStation
from src.simulation.base.intentions import Move, Pickup
from src.simulation.base.item import Item, ItemStatus
from src.simulation.environments.common import find_position_after_move, check_for_out_of_bounds_moves, IllegalMove, \
    enact_move_intention, group_intentions_by_item_to_pickup
from src.simulation.reactive_agents import TopCongestionAgent

class TestEnvironmentCommon(unittest.TestCase):
    def test_find_position_after_move(self):
        """Test that find_position_after_move returns the correct position after a move"""
        self.board = [[[] for _ in range(10)] for _ in range(10)]
        self.grid = Grid(self.board)
        self.agent = TopCongestionAgent((0, 0))
        move_intention = Move(self.agent.id, Move.RIGHT)
        self.grid.add_board_object(self.agent)

        position = find_position_after_move(move_intention, self.grid)
        self.assertEqual(position, (1, 0))

    def test_check_for_out_of_bound_moves(self):
        """Test that check_for_out_of_bounds_moves raises an exception when an agent tries to move out of bounds"""
        self.board = [[[] for _ in range(10)] for _ in range(10)]
        self.grid = Grid(self.board)
        self.agent = TopCongestionAgent((0, 0))
        move_intention = Move(self.agent.id, Move.LEFT)
        self.grid.add_board_object(self.agent)
        with self.assertRaises(IllegalMove):
            check_for_out_of_bounds_moves([move_intention], self.grid)

    def test_enact_move_intention(self):
        """Test that enact_move_intention moves the agent to the correct position"""
        self.board = [[[] for _ in range(10)] for _ in range(10)]
        self.grid = Grid(self.board)
        self.agent = TopCongestionAgent((0, 0))
        self.grid.add_board_object(self.agent)

        move_intention = Move(self.agent.id, Move.RIGHT)

        new_grid = enact_move_intention(move_intention, self.grid)
        self.assertEqual(new_grid.board[0][0], [])
        self.assertEqual(new_grid.board[1][0], [self.agent])

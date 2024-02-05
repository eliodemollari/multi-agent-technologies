import unittest
from src.simulation.base.grid import Grid
from src.simulation.base.intentions import Move
from src.simulation.environments.common import find_position_after_move, check_for_out_of_bounds_moves, IllegalMove, \
    enact_move_intention
from src.simulation.reactive_agents import TopCongestionAgent


class TestEnvironmentCommon(unittest.TestCase):
    def setUp(self):
        self.board = [[[] for _ in range(10)] for _ in range(10)]
        self.grid_size = [10, 10]
        self.test_grid = Grid(self.board, self.grid_size)

        self.agent = TopCongestionAgent((0, 0))
        self.test_grid.add_board_object(self.agent)

    def test_find_position_after_move_returns_correct_position(self):
        move_intention = Move(self.agent.id, Move.RIGHT)
        position = find_position_after_move(move_intention, self.test_grid)
        self.assertEqual(position, (1, 0))

    def test_check_for_out_of_bound_moves_raises_exception_when_agent_moves_out_of_bounds(self):
        move_intention = Move(self.agent.id, Move.LEFT)
        with self.assertRaises(IllegalMove):
            check_for_out_of_bounds_moves([move_intention], self.test_grid)

    def test_enact_move_intention_moves_agent_to_correct_position(self):
        move_intention = Move(self.agent.id, Move.RIGHT)
        new_grid = enact_move_intention(move_intention, self.test_grid)
        self.assertEqual(new_grid.board[0][0], [])
        self.assertEqual(new_grid.board[1][0], [self.agent])

    def tearDown(self):
        self.board = None
        self.grid_size = None
        self.test_grid = None
        self.agent = None

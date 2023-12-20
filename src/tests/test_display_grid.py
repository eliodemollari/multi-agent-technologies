import io
import sys
import unittest

from simulation.base.grid import Grid, PickupStation, DeliveryStation, Agent, Obstacle
from simulation.base.intentions import Intention
from simulation.simulation import display_grid


class TestAgent(Agent):
    def make_intention(self, grid: Grid) -> Intention:
        # Implement the method here
        pass


class TestDisplayGrid(unittest.TestCase):
    def setUp(self):
        pickup_stations = {}
        delivery_stations = {}
        agents = {}
        board = [[[] for _ in range(10)] for _ in range(10)]  # Create a 10x10 board of empty cells
        self.test_grid = Grid(pickup_stations, delivery_stations, agents, board)
        self.test_grid.add_board_object(PickupStation(), (1, 1))
        self.test_grid.add_board_object(DeliveryStation(), (2, 2))
        self.test_grid.add_board_object(TestAgent(), (3, 3))
        self.test_grid.add_board_object(TestAgent(), (3, 3))
        self.test_grid.add_board_object(TestAgent(), (3, 3))
        self.test_grid.add_board_object(TestAgent(), (1, 1))
        self.test_grid.add_board_object(Obstacle(), (4, 1))

    def test_display_grid_function(self):
        # Check the position of the PickupStation
        self.assertIsInstance(self.test_grid.board[1][1][0], PickupStation)

        # Check the position of the DeliveryStation
        self.assertIsInstance(self.test_grid.board[2][2][0], DeliveryStation)

        # Check the position of the Agents
        self.assertTrue(all(isinstance(obj, Agent) for obj in self.test_grid.board[3][3]))
        self.assertTrue(all(isinstance(obj, Agent) for obj in self.test_grid.board[1][1][1:]))

        original_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            display_grid(self.test_grid)
        finally:
            sys.stdout = original_stdout


if __name__ == '__main__':
    unittest.main()

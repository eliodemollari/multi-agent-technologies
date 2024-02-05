import io
import sys
import unittest

from src.simulation.base.grid import Agent, Grid, PickupStation, DeliveryStation, Obstacle
from src.simulation.reactive_agents import TopCongestionAgent
from src.simulation.simulation import display_grid


class TestDisplayGrid(unittest.TestCase):
    def setUp(self):
        board = [[[] for _ in range(10)] for _ in range(10)]  # Create a 10x10 board of empty cells
        grid_size = [10, 10]
        self.test_grid = Grid(board, grid_size)

        pickup_station = PickupStation((1, 1))
        delivery_station = DeliveryStation((2, 2))

        self.test_grid.add_board_object(pickup_station)
        self.test_grid.add_board_object(delivery_station)
        self.test_grid.add_board_object(TopCongestionAgent((1, 1)))
        self.test_grid.add_board_object(TopCongestionAgent((3, 3)))
        self.test_grid.add_board_object(TopCongestionAgent((3, 2)))
        self.test_grid.add_board_object(Obstacle((4, 1)))

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

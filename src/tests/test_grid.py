import unittest

from simulation.base.grid import DeliveryStation, PickupStation, find_element_in_grid, Grid


def sample_empty_3x3_board() -> list[list[list]]:
    return [[[], [], []], [[], [], []], [[], [], []]]


def empty_grid_from_board(board: list[list[list]]) -> Grid:
    return Grid({}, {}, {}, board)


class TestGrid(unittest.TestCase):
    def test_find_element_at_first_position(self):
        """Test that find_element_in_grid returns the correct position for an element at the first position in cell"""
        to_find = DeliveryStation()
        board = sample_empty_3x3_board()
        board[2][2] = [to_find]
        grid = empty_grid_from_board(board)
        position = find_element_in_grid(grid, to_find)
        self.assertEqual(position, (2, 2))

    def test_find_element_at_later_position(self):
        """Test that find_element_in_grid returns the correct position for an element at a later position in cell"""
        to_find = PickupStation()
        some_other_object = DeliveryStation()
        board = sample_empty_3x3_board()
        board[2][2] = [some_other_object, to_find]
        grid = empty_grid_from_board(board)
        position = find_element_in_grid(grid, to_find)
        self.assertEqual(position, (2, 2))

    def test_find_element_multiple_objects_of_class(self):
        """Test that find_element_in_grid returns the correct position for an element at a later position in cell, even
        if there are multiple objects of that class in the grid"""
        to_find = PickupStation()
        other_object_of_same_class = PickupStation()
        board = sample_empty_3x3_board()
        board[1][1] = [other_object_of_same_class]
        board[2][2] = [to_find]
        grid = empty_grid_from_board(board)
        position = find_element_in_grid(grid, to_find)
        self.assertEqual(position, (2, 2))

    def test_element_not_in_grid(self):
        """Test that find_element_in_grid returns None when the element is not in the grid"""
        to_find = PickupStation()
        board = sample_empty_3x3_board()
        grid = empty_grid_from_board(board)
        position = find_element_in_grid(grid, to_find)
        self.assertIsNone(position)

    def test_board_dimensions(self):
        """Test that board_dimensions returns the correct dimensions of the board"""
        board = sample_empty_3x3_board()
        grid = empty_grid_from_board(board)
        dimensions = grid.board_dimensions()
        self.assertEqual(dimensions, (3, 3))

    def test_add_board_object(self):
        """Test that add_board_object adds the object to the board"""
        board = sample_empty_3x3_board()
        grid = empty_grid_from_board(board)
        obj = PickupStation()
        grid.add_board_object(obj, (1, 1))
        self.assertEqual(grid.board[1][1], [obj])

    def test_add_board_object_multiple_objects(self):
        """Test that add_board_object adds the object to the board, even if there are other objects in the cell"""
        board = sample_empty_3x3_board()
        grid = empty_grid_from_board(board)
        obj = PickupStation()
        other_obj = DeliveryStation()
        grid.add_board_object(obj, (1, 1))
        grid.add_board_object(other_obj, (1, 1))
        self.assertEqual(grid.board[1][1], [obj, other_obj])

    def test_remove_board_object(self):
        """Test that remove_board_object removes the object from the board"""
        obj = PickupStation()
        board = sample_empty_3x3_board()
        board[1][1] = [obj]
        grid = empty_grid_from_board(board)
        grid.remove_board_object(obj, (1, 1))
        self.assertEqual(grid.board[1][1], [])

    def test_remove_board_object_multiple_objects(self):
        """Test that remove_board_object removes the object from the board, even if there are other objects at earlier
         positions in the cell"""
        obj = PickupStation()
        other_obj = DeliveryStation()
        board = sample_empty_3x3_board()
        board[1][1] = [other_obj, obj]
        grid = empty_grid_from_board(board)
        grid.remove_board_object(obj, (1, 1))
        self.assertEqual(grid.board[1][1], [other_obj])

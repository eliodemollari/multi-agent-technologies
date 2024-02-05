from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from src.simulation.base.grid import PickupStation, DeliveryStation, Obstacle


def find_shortest_path(state, agent_pos, station_pos):
    rows, cols = state.grid_size

    def get_matrix_element(x, y):
        if any(isinstance(item, Obstacle) for item in state.board[x][y]):
            return 0
        else:
            return 1

    matrix = [[get_matrix_element(y, x) for y in range(cols)] for x in range(rows)]
    grid = Grid(matrix=matrix)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(grid.node(agent_pos[0], agent_pos[1]), grid.node(station_pos[0], station_pos[1]), grid)
    next_node = path[1]

    return next_node.x, next_node.y


def tsp_path(state, agent_pos, station_pos):
    rows, cols = state.grid_size

    def get_matrix_element(x, y):
        if any(isinstance(item, Obstacle) for item in state.board[x][y]):
            return 1
        else:
            return 0

    matrix = [[get_matrix_element(y, x) for y in range(cols)] for x in range(rows)]
    grid = Grid(matrix=matrix, width=cols, height=rows, inverse=True)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(grid.node(agent_pos[0], agent_pos[1]), grid.node(station_pos[0], station_pos[1]), grid)

    return path

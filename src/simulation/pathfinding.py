from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from src.simulation.base.grid import PickupStation, DeliveryStation


def find_shortest_path(grid, grid_size, obstacles, agent_pos, station_pos, target_station=None, destination_station=None):
    # Unpack the grid size into rows and cols
    rows, cols = grid_size

    def get_matrix_element(x, y):
        if (x, y) in obstacles:
            return 0
        elif isinstance(grid.board[x][y], (PickupStation, DeliveryStation)) and (x, y) not in [target_station, destination_station]:
            return 0
        else:
            return 1

    matrix = [[get_matrix_element(x, y) for y in range(cols)] for x in range(rows)]
    grid = Grid(matrix=matrix)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(grid.node(agent_pos[0], agent_pos[1]), grid.node(station_pos[0], station_pos[1]), grid)
    next_node = path[1]

    return next_node.x, next_node.y

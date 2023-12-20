from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def find_shortest_path(grid_size, obstacles, agent_pos, station_pos):
    # Unpack the grid size into rows and cols
    rows, cols = grid_size

    def get_matrix_element(x, y):
        return 1 if (x, y) not in obstacles else 0

    matrix = [[get_matrix_element(x, y) for y in range(cols)] for x in range(rows)]
    grid = Grid(matrix=matrix)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(grid.node(agent_pos[0], agent_pos[1]), grid.node(station_pos[0], station_pos[1]), grid)
    next_node = path[1]

    return next_node.x, next_node.y

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from simulation.base.grid import Grid, PickupStation, DeliveryStation, Agent, Obstacle, BoardObject
from utils import logging_utils

# setup logger
logger = logging_utils.setup_logger('SimulationLogger', 'simulation.log')


def get_color(board_object: BoardObject) -> str:
    if isinstance(board_object, PickupStation):
        return 'green'
    elif isinstance(board_object, DeliveryStation):
        return 'blue'
    elif isinstance(board_object, Agent):
        return 'red'
    elif isinstance(board_object, Obstacle):
        return 'orange'
    else:
        logger.error(f"Unknown object in grid: {board_object}")
        raise ValueError(f"Unknown object in grid: {board_object}")


def display_grid(grid: Grid) -> None:
    fig, ax = plt.subplots()

    for row_idx, row in enumerate(grid.board):
        for col_idx, cell in enumerate(row):
            if len(cell) == 0:
                color = 'white'
                text = ''
            else:
                color = get_color(cell[0])
                agent_count = sum(isinstance(c, Agent) for c in cell)
                text = str(agent_count) if agent_count >= 1 else ''

            # Draw a rectangle for each cell
            rect = patches.Rectangle((col_idx, -row_idx - 1), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
            ax.add_patch(rect)

            # Display the number of items in the cell
            ax.text(col_idx + 0.5, -row_idx - 0.5, text, ha='center', va='center', color='white', fontsize=12,
                    weight='bold')

    ax.set_xlim(0, len(grid.board[0]))
    ax.set_ylim(-len(grid.board), 0)
    ax.set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()  # Invert y-axis to match grid coordinates

    # Remove labels from axes
    ax.set_xticks([])
    ax.set_yticks([])

    # Create a legend
    legend_elements = [patches.Patch(facecolor='green', edgecolor='black', label='Pickup'),
                       patches.Patch(facecolor='blue', edgecolor='black', label='Delivery'),
                       patches.Patch(facecolor='red', edgecolor='black', label='Agent'),
                       patches.Patch(facecolor='orange', edgecolor='black', label='Obstacle'),
                       patches.Patch(facecolor='white', edgecolor='black', label='Empty')]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0, 1.02))

    plt.show()

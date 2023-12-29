import argparse
import json

from src.simulation.base.environment import Environment
from src.simulation.base.grid import Grid, Obstacle, create_empty_board, PickupStation, DeliveryStation
from src.simulation.base.item import ItemStatus, Item
from src.simulation.environments.top_congestion_environment import TopCongestionEnvironment
from src.simulation.reactive_agents import TopCongestionAgent
from src.simulation.simulation import display_grid


def how_many_items_were_left_behind(environment: Environment) -> None:
    """Show the number of items left awaiting pickup per station, sorted in descending order"""
    stations = environment.state.pickup_stations
    items_left_behind = {station_id: len(station.items) for station_id, station in enumerate(stations)}
    items_left_behind_sorted = {k: v for k, v in sorted(items_left_behind.items(), key=lambda item: item[1],
                                                        reverse=True)}
    print(f"Items left behind: {items_left_behind_sorted}")


def top_deliver_agents(environment: Environment) -> None:
    """Show the number of delivered items per agent, sorted in descending order"""
    agents = environment.state.agents
    items_delivered = {agent_id: sum(1 for item in agent.items if item.status == ItemStatus.DELIVERED)
                       for agent_id, agent in enumerate(agents)}
    items_delivered_sorted = {k: v for k, v in sorted(items_delivered.items(), key=lambda item: item[1], reverse=True)}
    print(f"Top delivering agents: {items_delivered_sorted}")


def oldest_elements_in_stations(environment: Environment) -> None:
    """Shows the oldest item awaiting pickup in each station, using its creation tick, sorted in ascending order"""
    stations = environment.state.pickup_stations
    oldest_items = {station_id: min((item.created_tick for item in station.items), default=None)
                    for station_id, station in enumerate(stations)}
    # Remove stations with no items (None)
    oldest_items = {k: v for k, v in oldest_items.items() if v is not None}
    oldest_items_sorted = {k: v for k, v in sorted(oldest_items.items(), key=lambda item: item[1])}
    print(f"Oldest items in stations: {oldest_items_sorted}")


def analyze_results(environment: Environment) -> None:
    how_many_items_were_left_behind(environment)
    top_deliver_agents(environment)
    oldest_elements_in_stations(environment)


def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def setup_simulation(config) -> Environment:
    # Initialize the Grid
    grid_size = config['grid_size']
    board = create_empty_board(grid_size[0], grid_size[1])
    grid = Grid(board)

    # Initialize Obstacles
    for obstacle_coords in config['obstacles']:
        obstacle = Obstacle(obstacle_coords)
        grid.add_board_object(obstacle)

    # Initialize Pickup Stations
    for station_coords in config['pickup_stations']:
        pickup_station = PickupStation(station_coords)
        grid.add_board_object(pickup_station)

    # Initialize Delivery Stations
    for station_coords in config['delivery_stations']:
        delivery_station = DeliveryStation(station_coords)
        grid.add_board_object(delivery_station)

    for agent_coords in config['agents']:
        agent = TopCongestionAgent(agent_coords)
        grid.add_board_object(agent)

    for pickup_station in grid.pickup_stations:
        for i in range(2):
            pickup_station.items.append(
                Item(status=ItemStatus.AWAITING_PICKUP, created_tick=0, source=pickup_station,
                     destination=grid.delivery_stations[i]))

    return TopCongestionEnvironment(grid)


def run_simulation(environment: Environment, rounds: int) -> Environment:
    for i in range(rounds):
        environment.simulation_step()
    # display_grid(environment.state)

    return environment


def main(args):
    config = read_config(args.config_file)
    environment = setup_simulation(config)
    environment = run_simulation(environment, args.rounds)
    analyze_results(environment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a simulation based on a JSON configuration.")
    parser.add_argument('config_file', help="Path to the configuration JSON file.")
    parser.add_argument('--display', action='store_true', help="Display the grid after each step of the simulation.")
    parser.add_argument('--rounds', type=int, default=100, help="Number of simulation steps to run.")
    args = parser.parse_args()

    main(args)

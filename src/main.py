import argparse
import json

from simulation.base.environment import Environment
from simulation.base.grid import Grid, Obstacle, PickupStation, DeliveryStation, create_empty_board
from simulation.base.item import ItemStatus
from simulation.environments.top_congestion_environment import TopCongestionEnvironment
from simulation.item_factories.initial_distribution import InitialDistribution
from simulation.item_factories.weighted_distribution import WeightedDistribution
from simulation.reactive_agents import TopCongestionAgent
from simulation.simulation import display_grid


def how_many_items_were_left_behind(environment: Environment) -> None:
    """Show the number of items left awaiting pickup per station, sorted in descending order"""
    stations = environment.state.pickup_stations
    items_left_behind = {station_id: len(station.to_collect) for station_id, station in stations.items()}
    items_left_behind_sorted = {k: v for k, v in sorted(items_left_behind.items(), key=lambda item: item[1],
                                                        reverse=True)}
    print(f"Items left behind: {items_left_behind_sorted}")


def top_deliver_agents(environment: Environment) -> None:
    """Show the number of delivered items per agent, sorted in descending order"""
    agents = environment.state.agents
    items_delivered = {agent_id: sum(1 for item in agent.items if item.status == ItemStatus.DELIVERED)
                       for agent_id, agent in agents.items()}
    items_delivered_sorted = {k: v for k, v in sorted(items_delivered.items(), key=lambda item: item[1], reverse=True)}
    print(f"Top delivering agents: {items_delivered_sorted}")


def oldest_elements_in_stations(environment: Environment) -> None:
    """Shows the oldest item awaiting pickup in each station, using its creation tick, sorted in ascending order"""
    stations = environment.state.pickup_stations
    oldest_items = {station_id: min((item.created_tick for item in station.to_collect), default=None)
                    for station_id, station in stations.items()}
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
    grid = Grid({}, {}, {}, board)

    # Initialize Obstacles
    for obstacle_coords in config['obstacles']:
        obstacle = Obstacle()
        grid.add_board_object(obstacle, obstacle_coords)

    # Initialize Pickup Stations
    pickup_stations = {}
    for idx, station_coords in enumerate(config['pickup_stations'], start=1):
        pickup_station = PickupStation()
        pickup_stations[idx] = pickup_station
        grid.add_board_object(pickup_station, station_coords)
    grid.pickup_stations = pickup_stations

    # Initialize Delivery Stations
    delivery_stations = {}
    for idx, station_coords in enumerate(config['delivery_stations'], start=1):
        delivery_station = DeliveryStation()
        delivery_stations[idx] = delivery_station
        grid.add_board_object(delivery_station, station_coords)
    grid.delivery_stations = delivery_stations

    # Initialize Agents
    agents = {}
    for idx, agent_coords in enumerate(config['agents']):
        agent = TopCongestionAgent()
        agents[idx] = agent
        grid.add_board_object(agent, agent_coords)
    grid.agents = agents

    # Initialize the ItemFactory based on the strategy defined in the configuration
    if config['strategy'] == "InitialDistribution":
        # Convert string keys and values to integers
        if isinstance(config['distribution'], int):
            distribution = config['distribution']
        else:
            distribution = {
                int(k.split('_')[-1]): [int(v.split('_')[-1]) for v in vals]
                for k, vals in config['distribution'].items()
            }
        item_factory = InitialDistribution(distribution)
    elif config['strategy'] == "WeightedDistribution":
        # TODO: Make it a generic function, or something smarter in the first place
        pickup_distribution = {int(k.split('_')[-1]): int(v) for k, v in config['pickup_distribution'].items()}
        delivery_weights = {int(k.split('_')[-1]): int(v) for k, v in config['delivery_weights'].items()}
        steps_per_tick = config['steps_per_tick']
        item_factory = WeightedDistribution(pickup_distribution, delivery_weights, steps_per_tick)
    else:
        raise ValueError(f"Unknown strategy {config['strategy']}")

    return TopCongestionEnvironment(item_factory, grid)


def run_simulation(environment: Environment, rounds: int, display: bool = False) -> Environment:
    for _ in range(rounds):
        environment.simulation_step()
        if display:
            display_grid(environment.state)

    return environment


def main(args):
    config = read_config(args.config_file)
    environment = setup_simulation(config)
    environment = run_simulation(environment, args.rounds, args.display)
    analyze_results(environment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a simulation based on a JSON configuration.")
    parser.add_argument('config_file', help="Path to the configuration JSON file.")
    parser.add_argument('--display', action='store_true', help="Display the grid after each step of the simulation.")
    parser.add_argument('--rounds', type=int, default=100, help="Number of simulation steps to run.")
    args = parser.parse_args()

    main(args)

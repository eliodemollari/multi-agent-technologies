import argparse
import json

from src.simulation.base.environment import Environment
from src.simulation.base.grid import Grid, Obstacle, create_empty_board, PickupStation, DeliveryStation
from src.simulation.base.item import ItemStatus, Item
from src.simulation.environments.top_congestion_environment import TopCongestionEnvironment
from src.simulation.reactive_agents import TopCongestionAgent


def average_delivery_time_per_step(environment: Environment) -> None:
    """Calculate the average delivery time per simulation step for all delivered items"""
    agents = environment.state.agents
    delivery_times = [item.delivered_tick - item.created_tick for agent in agents
                      for item in agent.items if item.status == ItemStatus.DELIVERED]
    average_delivery_time = sum(delivery_times) / len(delivery_times) if delivery_times else 0
    average_delivery_time_per_step = average_delivery_time / environment.tick if environment.tick else 0
    print(f"Average delivery time per step: {average_delivery_time_per_step}")


def total_items_delivered(environment: Environment) -> None:
    """Calculate the total number of items delivered by each agent"""
    agents = environment.state.agents
    total_delivered = {}
    for i, agent in enumerate(agents):
        agent_items_delivered = sum(1 for item in agent.items if item.status == ItemStatus.DELIVERED)
        total_delivered[i] = agent_items_delivered
    print(f"Total items delivered: {total_delivered}")


def total_items_awaiting_pickup(environment: Environment) -> None:
    """Calculate the total number of items awaiting pickup at all stations"""
    stations = environment.state.pickup_stations
    total_awaiting_pickup = sum(len(station.items) for station in stations)
    print(f"Total items awaiting pickup: {total_awaiting_pickup}")


def total_items_assigned_to_agents(environment: Environment) -> None:
    """Calculate the total number of items assigned to agents at all stations"""
    agents = environment.state.agents
    total_items_assigned = {}
    for i, agent in enumerate(agents):
        agent_items_assigned = sum(1 for item in agent.items if item.status == ItemStatus.ASSIGNED_TO_AGENT)
        total_items_assigned[i] = agent_items_assigned
    print(f"Total items assigned to agent: {total_items_assigned}")


def total_items_in_transit(environment: Environment) -> None:
    """Calculate the total number of items in transit"""
    agents = environment.state.agents
    total_in_transit = sum(1 for agent in agents for item in agent.items if item.status == ItemStatus.IN_TRANSIT)
    print(f"Total items in transit: {total_in_transit}")


def agent_total_costs(environment: Environment) -> None:
    """Calculate the total cost of each agent"""
    agents = environment.state.agents
    costs = {agent_id: agent.total_cost for agent_id, agent in enumerate(agents)}
    print(f"Agent total costs: {costs}")


def agent_total_bundle_delivered(environment: Environment) -> None:
    """Calculate the total number of bundles delivered by each agent"""
    agents = environment.state.agents
    total_bundle_delivered = {}
    for i, agent in enumerate(agents):
        agent_bundle_delivered = 0
        for winner in agent.winner_bids:
            if all(item.status == ItemStatus.DELIVERED for item in winner['ordered_bundle']):
                agent_bundle_delivered += 1
        total_bundle_delivered[i] = agent_bundle_delivered
    print(f"Agent total number of delivered bundles: {total_bundle_delivered}")


def analyze_results(environment: Environment) -> None:
    total_items_delivered(environment)
    total_items_assigned_to_agents(environment)
    total_items_awaiting_pickup(environment)
    total_items_in_transit(environment)
    agent_total_costs(environment)
    agent_total_bundle_delivered(environment)


def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def setup_simulation(config) -> Environment:
    # Initialize the Grid
    grid_size = config['grid_size']
    board = create_empty_board(grid_size[0], grid_size[1])
    grid = Grid(board, grid_size)

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
        agent = TopCongestionAgent(agent_coords, 3)
        grid.add_board_object(agent)

    for pickup_station in grid.pickup_stations:
        for i in range(1):
            pickup_station.items.append(
                Item(status=ItemStatus.AWAITING_PICKUP, created_tick=0, source=pickup_station,
                     destination=grid.delivery_stations[i]))

    return TopCongestionEnvironment(grid)


def run_simulation(environment: Environment, rounds: int, selfishness: bool) -> Environment:
    for i in range(rounds):
        environment.simulation_step(selfishness)

    return environment


def main(args):
    config = read_config(args.config_file)
    environment = setup_simulation(config)
    environment = run_simulation(environment, args.rounds, args.selfishness)
    analyze_results(environment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a simulation based on a JSON configuration.")
    parser.add_argument('config_file', help="Path to the configuration JSON file.")
    parser.add_argument('--display', action='store_true', help="Display the grid after each step of the simulation.")
    parser.add_argument('--rounds', type=int, default=100, help="Number of simulation steps to run.")
    parser.add_argument('--selfishness', type=bool, help="Whether the agents should act selfishly or not.")
    args = parser.parse_args()

    main(args)

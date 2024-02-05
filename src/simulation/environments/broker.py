from src.simulation.base.grid import Grid
from src.simulation.base.item import ItemStatus
from src.utils import logging_utils
import itertools

logger = logging_utils.setup_logger('BrokerLogger', 'broker.log')


class Broker:
    def __init__(self, state: Grid):
        self.state = state
        self.items_available_for_auction = self._get_all_items_available_for_auction()
        self.agents = state.agents
        self.bids = self.announce_items()
        self.winners = self.auction_winners()

    def announce_items(self):
        bids = []
        for agent in self.agents:
            bids.append(agent.receive_auction_information(self.items_available_for_auction, self.state))
        return bids

    def auction_winners(self):
        # Flatten the data
        flat_data_bids = [item for sublist in self.bids for item in sublist]

        # Generate all combinations of bids
        bid_combinations = [combo for r in range(1, len(flat_data_bids) + 1) for combo in
                            itertools.combinations(flat_data_bids, r)]

        # Filter combinations to those that include all items exactly once
        valid_combinations = []
        for combo in bid_combinations:
            items = []
            for bid in combo:
                items += bid['ordered_bundle']
            if set(items) == set(self.items_available_for_auction) and len(items) == len(set(items)):
                valid_combinations.append(combo)

        # Find the combination with the lowest total cost
        lowest_cost = float('inf')
        best_combo = None
        for combo in valid_combinations:
            cost = sum(bid['costs'] for bid in combo)
            if cost < lowest_cost:
                lowest_cost = cost
                best_combo = combo

        return best_combo

    def assign_items_to_agents(self):
        logger.info("Assigning items to agents")
        print("Assigning items to agents")
        for winner in self.winners:
            agent = winner['agent']
            costs = winner['costs']
            agent.total_cost += costs
            for index, item in enumerate(winner['ordered_bundle']):
                agent.items.append(item)
                item.priority = index + 1  # Set the priority of the item
                item.agent_id = agent.id
                item.status = ItemStatus.ASSIGNED_TO_AGENT

                logger.info(f"Item {item.id} assigned to agent {agent.id}")
                print(f"Item {item.id} assigned to agent {agent.id}")

    def _get_all_items_available_for_auction(self):
        all_items = [item for station in self.state.pickup_stations for item in station.items if
                     item.status == ItemStatus.AWAITING_PICKUP]
        return all_items

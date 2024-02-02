from src.simulation.base.grid import Grid
from src.simulation.base.item import ItemStatus
from src.utils import logging_utils

logger = logging_utils.setup_logger('BrokerLogger', 'broker.log')


class Broker:
    def __init__(self, state: Grid):
        self.state = state
        self.items = self._get_all_items()
        self.items_available_for_auction = self._get_all_items_available_for_auction()
        self.agents = state.agents

    def announce_items(self):
        bids = []
        for agent in self.agents:
            bids.append(agent.receive_auction_information(self.items_available_for_auction, self.state))
        return bids

    def assign_items_to_agents(self):
        logger.info("Assigning items to agents")
        print("Assigning items to agents")
        for item in self.items:
            if item.status == ItemStatus.AWAITING_PICKUP:
                closest_agent = self.find_closest_agent(item.source.position)
                if closest_agent is not None:
                    closest_agent.items.append(item)
                    item.agent_id = closest_agent.id
                    item.status = ItemStatus.ASSIGNED_TO_AGENT
                    logger.info(f"Item {item.id} assigned to agent {closest_agent.id}")
                    print(f"Item {item.id} assigned to agent {closest_agent.id}")

    def find_closest_agent(self, position):
        available_agents = [agent for agent in self.agents if (not agent.is_assigned_item and not agent.is_carrying_item)]
        if not available_agents:
            return None
        return min(available_agents, key=lambda agent: self.calculate_distance(agent.position, position))

    def _get_all_items(self):
        all_items = [item for station in self.state.pickup_stations for item in station.items]
        return all_items

    def _get_all_items_available_for_auction(self):
        all_items = [item for station in self.state.pickup_stations for item in station.items if item.status == ItemStatus.AWAITING_PICKUP]
        return all_items

    @staticmethod
    def calculate_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

from src.simulation.base.grid import Grid
from src.simulation.base.item import ItemStatus
from src.utils import logging_utils

logger = logging_utils.setup_logger('Brokerlogger', 'broker.log')


class Broker:
    def __init__(self, state: Grid):
        self.state = state
        self.items = self._get_all_items()
        self.agents = state.agents

    def assign_items_to_agents(self):
        logger.info(f"Broker assigning items to agents")
        print(f"Broker assigning items to agents")
        # intentions = []
        for item in self.items:
            if item.status == ItemStatus.AWAITING_PICKUP:
                closest_agent = self.find_closest_agent(item.source.position)
                if closest_agent is not None:
                    closest_agent.items.append(item)
                    item.agent_id = closest_agent.id
                    item.status = ItemStatus.ASSIGNED_TO_AGENT
                    # intention = closest_agent.make_intention(self.state)
                    # intentions.append(intention)
        # return intentions

    def recommend_agents(self, item):
        print(f"Broker recommending top 3 available agents for item")
        logger.info(f"Broker recommending top 3 available agents for item")
        recommended_agents = []
        if item.status == ItemStatus.AWAITING_PICKUP:
            closest_agent = self.find_three_most_closest_agents(item.source.position)
            if closest_agent is not None:
                recommended_agents.append(closest_agent)

    def find_three_most_closest_agents(self, position):
        logger.info(f"Broker finding three most closest agents")
        available_agents = [agent for agent in self.agents if (not agent.is_assigned_item and not agent.is_carrying_item)]
        if not available_agents:
            return None
        return sorted(available_agents, key=lambda agent: self.calculate_distance(agent.position, position))[:3]

    def find_closest_agent(self, position):
        logger.info(f"Broker finding closest agent")
        available_agents = [agent for agent in self.agents if (not agent.is_assigned_item and not agent.is_carrying_item)]
        if not available_agents:
            return None
        return min(available_agents, key=lambda agent: self.calculate_distance(agent.position, position))

    def _get_all_items(self):
        logger.info(f"Broker getting all items")
        all_items = [item for station in self.state.pickup_stations for item in station.items]
        return all_items

    @staticmethod
    def calculate_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

from src.simulation.base.grid import Grid
from src.simulation.base.item import ItemStatus


class Broker:
    def __init__(self, state: Grid):
        self.state = state
        self.items = self._get_all_items()
        self.agents = state.agents

    def assign_items_to_agents(self):
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

    def find_closest_agent(self, position):
        available_agents = [agent for agent in self.agents if not agent.is_assigned_item]
        if not available_agents:
            return None
        return min(available_agents, key=lambda agent: self.calculate_distance(agent.position, position))

    def _get_all_items(self):
        all_items = [item for station in self.state.pickup_stations for item in station.items]
        return all_items

    @staticmethod
    def calculate_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

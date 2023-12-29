import unittest
from src.simulation.base.grid import Agent
from src.simulation.environments.broker import Broker
from src.simulation.base.item import Item, ItemStatus
from src.simulation.base.grid import PickupStation, DeliveryStation


class TestBroker(unittest.TestCase):
    def setUp(self):
        self.agents = [Agent((i, i)) for i in range(5)]
        self.items = [
            Item(
                status=ItemStatus.AWAITING_PICKUP,
                created_tick=0,
                source=PickupStation((i, i)),
                destination=DeliveryStation((i+1, i+1))
            ) for i in range(5)
        ]
        self.broker = Broker(self.items, self.agents)

    def test_assign_items_to_agents(self):
        self.broker.assign_items_to_agents()
        for agent in self.agents:
            self.assertIsNotNone(agent.intention)

if __name__ == '__main__':
    unittest.main()
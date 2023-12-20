import unittest

from simulation.item_factories.initial_distribution import InitialDistribution
from simulation.item_factories.common import StationDoesNotExist
from tests.test_distributions_common import setup_grid


class TestInitialDistribution(unittest.TestCase):
    def setUp(self):
        self.state = setup_grid()
        self.tick = 0

    def test_simple_distribution(self):
        # Test case for integer distribution
        distribution = 3
        initial_distribution = InitialDistribution(distribution)
        updated_state = initial_distribution.add_items(self.state, self.tick)

        # Assert that each pickup station has 3 items with random destinations
        for pickup_station in updated_state.pickup_stations.values():
            self.assertEqual(len(pickup_station.to_collect), distribution)
            for item in pickup_station.to_collect:
                self.assertIn(item.destination, updated_state.delivery_stations.keys())

    def test_exact_distribution(self):
        # Test case for dictionary distribution
        distribution = {
            1: [2, 3, "a"],
            2: ["c", "b", 2, 3]
        }
        initial_distribution = InitialDistribution(distribution)
        updated_state = initial_distribution.add_items(self.state, self.tick)

        # Assert that each pickup station has items with the specified destinations
        for source_station, targets in distribution.items():
            pickup_station = updated_state.pickup_stations[source_station]
            self.assertEqual(len(pickup_station.to_collect), len(targets))
            for item, destination_station in zip(pickup_station.to_collect, targets):
                self.assertEqual(item.destination, destination_station)

    def test_bad_distribution_source(self):
        # Test that a StationDoesNotExist exception is raised when a source station in the distribution does not exist
        distribution = {
            1: [2, 3, "a"],
            5: ["c", "b", 2, 3],
            10: [1, 2, 3]
        }
        with self.assertRaises(StationDoesNotExist):
            initial_distribution = InitialDistribution(distribution)
            initial_distribution.add_items(self.state, self.tick)

    def test_bad_distribution_target(self):
        # Test that a StationDoesNotExist exception is raised when a target station in the distribution does not exist
        distribution = {
            1: [2, 3, "a"],
            2: ["d", "e", "f"]
        }
        initial_distribution = InitialDistribution(distribution)
        with self.assertRaises(StationDoesNotExist):
            initial_distribution.add_items(self.state, self.tick)

    def test_tick_not_zero(self):
        # Test when tick is not zero
        distribution = 3
        initial_distribution = InitialDistribution(distribution)
        self.tick = 1
        updated_state = initial_distribution.add_items(self.state, self.tick)

        # Assert that the state remains unchanged
        self.assertEqual(updated_state, self.state)

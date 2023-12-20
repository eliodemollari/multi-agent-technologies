import unittest

from simulation.item_factories.common import StationDoesNotExist
from simulation.item_factories.weighted_distribution import WeightedDistribution
from tests.test_distributions_common import setup_grid


class TestWeightedDistribution(unittest.TestCase):
    def setUp(self):
        self.state = setup_grid()

    def test_bad_distribution_source(self):
        # Test that a StationDoesNotExist exception is raised when a source station in the distribution does not exist
        distribution = {
            1: 0.3,
            5: 0.6,
            10: 1
        }
        delivery_weights = {
            1: 1,
            "b": 10,
            3: 0
        }
        with self.assertRaises(StationDoesNotExist):
            weighted_distribution = WeightedDistribution(distribution, delivery_weights, steps_per_tick=10)
            weighted_distribution.add_items(self.state, tick=0)

    def test_bad_distribution_target(self):
        # Test that a StationDoesNotExist exception is raised when a target station in the distribution does not exist
        distribution = {
            1: 0.3,
            2: 0.6,
        }
        delivery_weights = {
            1: 1,
            "z": 10,
            3: 0
        }
        with self.assertRaises(StationDoesNotExist):
            weighted_distribution = WeightedDistribution(distribution, delivery_weights, steps_per_tick=10)
            weighted_distribution.add_items(self.state, tick=0)

    def test_constant_source_distribution(self):
        """Confirm that with distribution of 1.0 for all pickup stations, the number of items added is equal to the
        number of steps per tick"""
        distribution = {
            1: 1.0,
            2: 1.0,
        }
        delivery_weights = {
            1: 1,
            "b": 10,
            3: 0
        }
        steps_per_tick = 10
        weighted_distribution = WeightedDistribution(distribution, delivery_weights, steps_per_tick)
        updated_state = weighted_distribution.add_items(self.state, tick=0)
        for pickup_station in updated_state.pickup_stations.values():
            self.assertEqual(len(pickup_station.to_collect), steps_per_tick)

    def test_zero_source_distribution(self):
        """Confirm that with distribution of 0.0 for all pickup stations, no items are added"""
        distribution = {
            1: 0.0,
            2: 0.0,
        }
        delivery_weights = {
            1: 1,
            "b": 10,
            3: 0
        }
        steps_per_tick = 10
        weighted_distribution = WeightedDistribution(distribution, delivery_weights, steps_per_tick)
        updated_state = weighted_distribution.add_items(self.state, tick=0)
        for pickup_station in updated_state.pickup_stations.values():
            self.assertEqual(len(pickup_station.to_collect), 0)

    def test_skewed_destination_weights(self):
        """Test that when all but one station will have weights equal to 0, the items will be added only to the
        non-zero station"""
        distribution = {
            1: 1.0,
            2: 1.0,
        }
        delivery_weights = {
            1: 0,
            "b": 0,
            3: 1
        }
        steps_per_tick = 10
        weighted_distribution = WeightedDistribution(distribution, delivery_weights, steps_per_tick)
        updated_state = weighted_distribution.add_items(self.state, tick=0)
        for pickup_station in updated_state.pickup_stations.values():
            self.assertEqual(len(pickup_station.to_collect), steps_per_tick)
            for item in pickup_station.to_collect:
                self.assertEqual(item.destination, 3)

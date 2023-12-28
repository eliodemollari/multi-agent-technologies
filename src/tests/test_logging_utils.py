import unittest
import logging
import os
from src.utils import logging_utils
from src.simulation.base.item import Item, ItemStatus


class TestItemLogging(unittest.TestCase):
    def setUp(self):
        self.log_file = os.path.join(os.getcwd(), 'item.log')
        self.logger = logging_utils.setup_logger('ItemLogger', self.log_file)

    def test_item_creation_logs_message(self):
        item = Item(1, 1, 2, ItemStatus.AWAITING_PICKUP)
        with open(self.log_file, 'r') as f:
            log_messages = f.readlines()
        self.assertGreater(len(log_messages), 0)
        self.assertIn("Item created with tick 1, source 1, destination 2, status ItemStatus.AWAITING_PICKUP", log_messages[-1])


class TestLoggingUtils(unittest.TestCase):
    def setUp(self):
        self.log_file = os.path.join(os.getcwd(), 'test.log')
        self.logger = logging_utils.setup_logger('TestLogger', self.log_file)

    def test_setup_logger(self):
        self.assertIsInstance(self.logger, logging.Logger)
        self.assertEqual(self.logger.name, 'TestLogger')
        self.assertEqual(self.logger.level, logging.INFO)
        self.assertEqual(len(self.logger.handlers), 1)
        self.assertIsInstance(self.logger.handlers[0], logging.FileHandler)
        self.assertEqual(self.logger.handlers[0].baseFilename, self.log_file)


if __name__ == '__main__':
    unittest.main()

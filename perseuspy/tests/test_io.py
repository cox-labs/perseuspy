from unittest import TestCase
from os import path
from perseuspy import pd

TEST_DIR = path.dirname(__file__)

class TestReading(TestCase):
    def test_reading_example(self):
        df = ps.read_perseus(path.join(TEST_DIR, 'matrix.txt'))
	self.assertIsNot(df, None)

from unittest import TestCase
from os import path
from io import StringIO
from perseuspy import pd

TEST_DIR = path.dirname(__file__)

class TestReading(TestCase):
    def test_reading_example1(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix.txt'))
        self.assertIsNot(df, None)
        out = StringIO()
        df.to_perseus(out)
        self.assertIsNot(str(out), '')

    def test_reading_example2(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix2.txt'))
        self.assertIsNot(df, None)
        out = StringIO()
        df.to_perseus(out)
        self.assertIsNot(str(out), '')

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

    def test_inferring_and_setting_main_columns(self):
        def typeRow(df, main_columns=None):
            out = StringIO()
            df.to_perseus(out, main_columns)
            out.seek(0)
            typeRow = out.readlines()[1]
            return typeRow

        df = pd.DataFrame({'a' : [2,3], 'b': [1,2], 'c': ['a','b'], 'd': [3,4]})
        self.assertEqual('#!{Type}E\tE\tT\tN\n', typeRow(df))
        self.assertEqual('#!{Type}N\tE\tT\tE\n', typeRow(df, main_columns={'b','d'}))

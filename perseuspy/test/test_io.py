from unittest import TestCase, main
from os import path
from io import StringIO
from perseuspy import pd

TEST_DIR = path.dirname(__file__)

def to_string(df, **kwargs):
    out = StringIO()
    df.to_perseus(out, **kwargs)
    out.seek(0)
    return '\n'.join(out.readlines())

def type_row(df, **kwargs):
    lines = to_string(df, **kwargs).splitlines()
    for line in lines:
        if line.startswith('#!{Type}'):
            return line.strip()
    return ''

class TestReading(TestCase):
    def test_reading_example1(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix.txt'))
        self.assertIsNot(df, None)
        self.assertIsNot(to_string(df), '')
        self.assertEqual('#!{Type}' + (15 * 'E\t') + 'T', type_row(df))

    def test_reading_example2(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix2.txt'))
        self.assertIsNot(df, None)
        self.assertIsNot(to_string(df), '')

    def test_reading_example3(self):
        df = pd.read_perseus(path.join(TEST_DIR, 'matrix3.txt'))
        self.assertIsNot(df, None)
        self.assertIsNot(to_string(df), '')
        self.assertEqual('#!{Type}' + (3 * 'E\t') + 'C',
                '\t'.join(type_row(df).split('\t')[:4]))

    def test_inferring_and_setting_main_columns(self):
        df = pd.DataFrame({'a' : [2,3], 'b': [1,2], 'c': ['a','b'], 'd': [3,4]})
        self.assertEqual('#!{Type}E\tE\tT\tN', type_row(df))
        self.assertEqual('#!{Type}N\tE\tT\tE', type_row(df, main_columns={'b','d'}))

if __name__ == '__main__':
    main()

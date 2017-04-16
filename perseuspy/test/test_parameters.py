from unittest import TestCase, main
from os import path
from perseuspy.parameters import *

TEST_DIR = path.dirname(__file__)

class TestParameters(TestCase):

    def setUp(self):
        self.parameters = parse_parameters(path.join(TEST_DIR, 'parameters.xml'))

    def test_int_param(self):
        self.assertEqual(15, intParam(self.parameters, 'Number of columns'))

    def test_double_param(self):
        self.assertEqual(2.0, doubleParam(self.parameters, 'Box size'))

    def test_file_param(self):
        self.assertEqual('some_file.txt', fileParam(self.parameters, 'someFile.txt'))

    def test_single_choice_param(self):
        self.assertEqual('Two normal distributions', singleChoiceParam(self.parameters, 'Mode'))

if __name__ == '__main__':
    main()

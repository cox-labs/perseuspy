from unittest import TestCase, main
from os import path
from perseuspy.parameters import *

TEST_DIR = path.dirname(__file__)

class TestParameters(TestCase):

    def setUp(self):
        self.parameters = parse_parameters(path.join(TEST_DIR, 'parameters.xml'))

    def test_int_param(self):
        self.assertEqual(15, intParam(self.parameters, 'Number of columns'))

    def test_int_param2(self):
        self.assertEqual(-15, intParam(self.parameters, 'Test int param'))

    def test_double_param(self):
        self.assertEqual(2.0, doubleParam(self.parameters, 'Box size'))

    def test_file_param(self):
        self.assertEqual('some_file.txt', fileParam(self.parameters, 'someFile.txt'))

    def test_single_choice_param(self):
        self.assertEqual('Two normal distributions', singleChoiceParam(self.parameters, 'Mode'))

    def test_single_choice_param_no_value_chosen(self):
        self.assertEqual(-1, singleChoiceParam(self.parameters, 'Test'))

    def test_multi_choice_param(self):
        self.assertEqual(['T', 'Y'], multiChoiceParam(self.parameters, 'Select'))

    def test_single_choice_with_subparams(self):
        value, subparams = singleChoiceWithSubParams(self.parameters, 'Choose')
        self.assertEqual('B', value)
        self.assertEqual(3.0, doubleParam(subparams, 'Sub'))

    def test_bool_with_subparams(self):
        value, subparam = boolWithSubParams(self.parameters, 'Choose bool')
        self.assertTrue(value)
        self.assertEqual('false', stringParam(subparam, 'Sub'))

    def test_bool_with_subparams2(self):
        value, subparam = boolWithSubParams(self.parameters, 'Choose bool 2')
        self.assertFalse(value)
        self.assertEqual(0, len(subparam))

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
__author__ = 'guti'

from context import core

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """
    Advanced test cases for exception.
    """
    def check_input_line_test(self):
        with self.assertRaises(ValueError):
            core.check_input_line('2016-02-30 09:00~11:00 7')
        with self.assertRaises(ValueError):
            core.check_input_line('2016-10-01 0s8:00~11:00 4')
        with self.assertRaises(ValueError):
            core.check_input_line('2016-10-20 09:00~22:00 a')
        with self.assertRaises(AssertionError):
            core.check_input_line('2016-10-31 10:00~09:00 11')

    def payment_list_test(self):
        from copy import deepcopy
        strategy = deepcopy(core.CHARGE_STRATEGY[('Sat', 'Sun')])
        with self.assertRaises(AssertionError):
            core.payment_list('11:00~11:00', strategy)


if __name__ == '__main__':
    unittest.main()
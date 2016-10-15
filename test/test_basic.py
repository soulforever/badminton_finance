# -*- coding: utf-8 -*-
__author__ = 'guti'

from context import core

import unittest


class BasicTestSuite(unittest.TestCase):
    """
    Basic test cases for functions in core.
    """
    def test_courts(self):
        assert core.courts(3) == 0
        assert core.courts(4) == 1
        assert core.courts(6) == 2
        assert core.courts(12) == 2
        assert core.courts(18) == 3
        assert core.courts(30) == 5

    def income_test(self):
        assert core.income(60) == 1800
        assert core.income(5) == 150
        assert core.income(0) == 0

    def payment_test(self):
        assert core.payment([(1, 30), (6, 50), (2, 80)]) == 510
        assert core.payment([(1, 30)]) == 30

    def info_rows_test(self):
        test_iter = ['2016-10-15 10:00~13:00 11']
        assert core.info_rows(test_iter)[2] == '2016-10-15 10:00~13:00 +330 -260 70'
        test_iter.append('2016-10-17 09:00~18:00 12')
        assert core.info_rows(test_iter)[3] == '2016-10-17 09:00~18:00 +360 -780 -420'
        test_iter.append('2016-10-18 12:00~22:00 6')
        assert core.info_rows(test_iter)[4] == '2016-10-18 12:00~22:00 +180 -1160 -980'

    def payment_list_test(self):
        strategy = core.CHARGE_STRATEGY[('Mon', 'Tue', 'Wed', 'Thu', 'Fri')]
        time_range = '10:00~17:00'
        assert core.payment_list(time_range, strategy) == [(2, 30), (5, 50)]
        strategy = core.CHARGE_STRATEGY[('Sat', 'Sun')]
        time_range = '19:00~22:00'
        assert core.payment_list(time_range, strategy) == [(3, 60)]


if __name__ == '__main__':
    unittest.main()

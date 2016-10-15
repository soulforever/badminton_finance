# -*- coding: utf-8 -*-
__author__ = 'guti'

'''
Helper module for badminton_finance.
'''

import datetime
import logging

# incomes from every applicant
INCOMES_PER_APPLICANT = 30

# the applicant for each court usually.
APPLICANTS_PER_COURT = 6

# oder strategy
ODER_STRATEGY = {
    # (x, y) means the x <= numbers_of_applicants / applicants_per_court <= y
    (0, 0): {
        # the condition (x, y) means x <= numbers_of_applicants % applicants_per_court <= y
        (0, 3): 'same',
        (4, 5): 'plus',
    },
    (1, 1): {
        # the condition (None, None) means in any condition
        (None, None): 'plus'
    },
    (2, 3): {
        (0, 3): 'same',
        (4, 5): 'plus',
    },
    # (x, None) means the numbers_of_applicants / applicants_per_court >= x
    (4, None): {
        (None, None): 'same'
    }
}

# charges of the court
CHARGE_STRATEGY = {
    ('Mon', 'Tue', 'Wed', 'Thu', 'Fri'): {
        ('09:00', '12:00'): 30,
        ('12:00', '18:00'): 50,
        ('18:00', '20:00'): 80,
        ('20:00', '22:00'): 60,
    },
    ('Sat', 'Sun'): {
        ('09:00', '12:00'): 40,
        ('12:00', '18:00'): 50,
        ('18:00', '22:00'): 60,
    },
}


def value_for(number, config_dict):
    """
    A helper function to find key in config dict.

    :param number: int, the number to find range key.
    :param config_dict: dict, keys are tuple to define the range.
    :return: tuple, keys.

    Usage::
        >>> value_for(0, ODER_STRATEGY)[(0, 3)]
        'same'
        >>> value_for(4, ODER_STRATEGY[(1, 1)])
        'plus'
        >>> value_for(3, ODER_STRATEGY[(0, 0)])
        'same'
        >>> value_for(-1, ODER_STRATEGY)
        Traceback (most recent call last):
        ...
        AttributeError: Can not find the range for number in the config.
    """
    for key in config_dict.iterkeys():
        start, end = key
        if (start is None and end is None) or (start is None and number <= end) or \
                (end is None and number >= start) or (start <= number <= end):
            return config_dict[key]
    raise AttributeError('Can not find the range for number in the config.')


def convert_time_str_tuple(str_tuple):
    """
    Help function for convert a time string tuple to datetime object tuple.
    :param str_tuple: tuple, formed by time string.
    :return: tuple, formed by time object
    """
    return tuple([datetime.datetime.strptime(time_str, '%H:%M') for time_str in str_tuple])


def _check_strategy():
    """
    Help function for check legality of CHARGE_STRATEGY
    """
    assert_str = 'Config in CHARGE_STRATEGY is illegal.'
    for week, strategy in CHARGE_STRATEGY.iteritems():
        for item in week:
            assert item in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'), assert_str
        for k, v in strategy.iteritems():
            start_k, end_k = convert_time_str_tuple(k)
            assert start_k < end_k, assert_str
            assert v > 0, assert_str

# assert the strategy is legal
_check_strategy()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import doctest
    doctest.testmod()

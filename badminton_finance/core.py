# -*- coding: utf-8 -*-
__author__ = 'guti'

'''
A module calculate the cost of ordering badminton court.
'''

import logging
import datetime
import re

from helpers import INCOMES_PER_APPLICANT, APPLICANTS_PER_COURT, ODER_STRATEGY, CHARGE_STRATEGY
from helpers import value_for, convert_time_str_tuple

# regular expression for input string
_RE_DATE = re.compile(r'\d{4}-((0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-8])|(0[13-9]|1[0-2])-(29|30)|(0[13578]|1[02])-31)')
_RE_TIME = re.compile(r'((09|1[0-9]|2[012]):00)~((09|1\d|2[012]):00)')
_RE_NUM = re.compile(r'\d+')


def check_input_line(format_str_line):
    """
    Check the legality of input line.
    :param format_str_line: str, one line input.
    :return: None.
    """
    input_list = format_str_line.split()
    assert len(input_list), 'Input information is not complete.'
    re_list = [_RE_DATE, _RE_TIME, _RE_NUM]
    for i in range(3):
        # check the format
        m = re_list[i].match(input_list[i])
        if m is None:
            raise ValueError('Input string is not match the format. %s' % format_str_line)
        # check the time range.
        if i == 1:
            start, end = convert_time_str_tuple((m.group(1), m.group(3)))
            assert start < end, 'start time must less than end time.'


def courts(applicants):
    """
    Calculate the courts for all applicants by using the strategy config.

    :param applicants: int, numbers of applicants.
    :return: int, courts will order.

    Usage::
        >>> courts(3)
        0
        >>> courts(5)
        1
        >>> courts(7)
        2
        >>> courts(29)
        4
    """
    quotient, remainder = divmod(applicants, APPLICANTS_PER_COURT)
    strategy_str = value_for(remainder, value_for(quotient, ODER_STRATEGY))
    if strategy_str == 'same':
        return quotient
    elif strategy_str == 'plus':
        return quotient + 1
    else:
        logging.warning(strategy_str)
        raise ValueError('Can not resolve the strategy string.')


def income(applicants):
    """
    Calculate the income from applicants.

    :param applicants: int, numbers of applicants.
    :return: int, income from the applicants.
    """
    return applicants * INCOMES_PER_APPLICANT


def payment(exp_list):
    """
    Calculate the payment by the hours and payment per_hour.

    :param exp_list: list, formed by tuple with hours and payment.
    :return: int, payment calculated by the information of the payment list.

    Usage::
        >>> payment([(3, 50)])
        150
        >>> payment([(2,40), (3, 50)])
        230
    """
    return sum(hours * payment_per_hour for (hours, payment_per_hour) in exp_list)


def day_of_week(data_str):
    """
    Check the date, weekday or weekend

    :param data_str: str, format as '%Y-%m-%d' like '2016-06-02'
    :return: str, weekday or weekend

    Usage::
        >>> day_of_week('2016-10-14')
        'Fri'
        >>> day_of_week('2016-10-15')
        'Sat'
        >>> day_of_week('2016-10-18')
        'Tue'
    """
    date = datetime.datetime.strptime(data_str, '%Y-%m-%d')
    return date.strftime('%a')


def _payment_list_driver(hour_range_tuple, charge_strategy, result_list):
    """
    Help function for generating payment list,
    items of the list is a tuple with hours and payment per hour in these hours.

    :param hour_range_tuple: tuple, range of hours, formed by datetime object.
    :param charge_strategy: dict, charge strategy of the day.
    :param result_list: list, items are tuple formed by hours and charge.
    :return: list

    Usage::
        >>> time_1 = datetime.datetime.strptime('20:00', '%H:%M')
        >>> time_2 = datetime.datetime.strptime('22:00', '%H:%M')
        >>> _payment_list_driver((time_1, time_2), CHARGE_STRATEGY[('Mon', 'Tue', 'Wed', 'Thu', 'Fri')], [])
        [(2, 60)]
        >>> time_1 = datetime.datetime.strptime('10:00', '%H:%M')
        >>> time_2 = datetime.datetime.strptime('13:00', '%H:%M')
        >>> _payment_list_driver((time_1, time_2), CHARGE_STRATEGY[('Mon', 'Tue', 'Wed', 'Thu', 'Fri')], [])
        [(2, 30), (1, 50)]
        >>> time_1 = datetime.datetime.strptime('20:00', '%H:%M')
        >>> time_2 = datetime.datetime.strptime('22:00', '%H:%M')
        >>> _payment_list_driver((time_1, time_2), CHARGE_STRATEGY[('Mon', 'Tue', 'Wed', 'Thu', 'Fri')], [])
        [(2, 60)]
    """
    start, end = hour_range_tuple
    assert start < end, 'start time must less than end time.'
    for key in charge_strategy:
        start_k, end_k = convert_time_str_tuple(key)
        if start_k <= start < end_k:
            if end <= end_k:
                result_list.append(((end - start).seconds/3600, charge_strategy[key]))
                return result_list
            else:
                result_list.append(((end_k - start).seconds/3600, charge_strategy[key]))
                return _payment_list_driver((end_k, end), charge_strategy, result_list)


def payment_list(hour_range_str, charge_strategy):
    """
    A wrapper for _payment_list_driver.

    :param hour_range_str: str, range of hours, like '9:00~13:00'.
    :param charge_strategy: dict, charge strategy of the day.
    :return: list

    Usage::
        >>> payment_list('12:00~15:00', CHARGE_STRATEGY[('Sat', 'Sun')])
        [(3, 50)]
        >>> payment_list('20:00~22:00', CHARGE_STRATEGY[('Mon', 'Tue', 'Wed', 'Thu', 'Fri')])
        [(2, 60)]
    """
    hour_range_tuple = convert_time_str_tuple(hour_range_str.split('~'))
    return _payment_list_driver(hour_range_tuple, charge_strategy, [])


def info_single(format_str_line):
    """
    Generate a information dict by calculating a line of format string.
    :param format_str_line: str, one line string,
                            with the format: {date} {start_time~end_time} {numbers of applicants}.
    :return: dict, contains information of payment and income.
    Usage::

        >>> info_single('2016-06-02 20:00~22:00 7')['payment']
        240
        >>> info_single('2016-06-09 16:00~18:00 16')['profit']
        180
    """
    date_str, hour_range_str, applicants_str = format_str_line.split()
    applicants = int(applicants_str)
    numbers_courts = courts(applicants)
    # calculate the income
    inc = income(applicants) if numbers_courts > 0 else 0

    # calculate the payment
    charge_strategy = None
    week_str = day_of_week(date_str)
    for k, v in CHARGE_STRATEGY.iteritems():
        if week_str in k:
            charge_strategy = v
    if not charge_strategy:
        raise AttributeError('Can not found information of this day of week in config.')
    exp = payment(payment_list(hour_range_str, charge_strategy)) * numbers_courts

    # calculate the profit, use '+' because the payment in negative
    bal = inc - exp

    # use the time string as key of the return dict
    time = date_str + ' ' + hour_range_str
    # format the return dict
    return dict(time=time, income=inc, payment=exp, profit=bal)


def info_rows(info_iter):
    """
    Generate a information list with all time information as key and profit information dict as value.

    :param info_iter: iterable, formed by string of ordering information.
    :return: list, formed by out put strings.

    Usage::

        >>> info_iter = ['2016-06-02 20:00~22:00 7', '2016-06-03 09:00~12:00 14']
        >>> info_rows(info_iter)[2:4]
        ['2016-06-02 20:00~22:00 +210 -240 -30', '2016-06-03 09:00~12:00 +420 -180 +240']
        >>> info_rows(info_iter)[-3:]
        ['Total Income: 630', 'Total Payment: 420', 'Profit: 210']
        >>> info_iter.append('2016-06-05 19:00~22:00 3')
        >>> info_rows(info_iter)[4]
        '2016-06-05 19:00~22:00 +0 -0 0'
    """
    # init
    output_list = list()
    total_income, total_payment, total_profit = 0, 0, 0

    # set title
    title = ['[Summary]', '']
    output_list.extend(title)
    for line in info_iter:
        info = info_single(line)
        # count for total
        total_income += info['income']
        total_payment += info['payment']
        total_profit += info['profit']
        # get format string
        info['profit'] = '%+d' % info['profit'] if info['profit'] != 0 else str(info['profit'])
        format_str = '{time} +{income} -{payment} {profit}'.format(**info)
        output_list.append(format_str)

    # set footer
    footer = ['', 'Total Income: {}'.format(total_income), 'Total Payment: {}'.format(total_payment),
              'Profit: {}'.format(total_profit)]
    output_list.extend(footer)
    return output_list


def info_rows_generator(info_iter):
    """
    A generator of information.

    :param info_iter: iterable, formed by string of ordering information.
    :yield: str, out put string with total information.
    """
    total_income, total_payment, total_profit = 0, 0, 0
    title = ['[Summary]', '']
    for line in title:
        yield line
    for format_str_line in info_iter:
        info = info_single(format_str_line)
        total_income += info['income']
        total_payment += info['payment']
        total_profit += info['profit']
        info['profit'] = '%+d' % info['profit'] if info['profit'] != 0 else str(info['profit'])
        format_str = '{time} +{income} -{payment} {profit}'.format(**info)
        yield format_str
    footer = ['', 'Total Income: {}'.format(total_income), 'Total Payment: {}'.format(total_payment),
              'Profit: {}'.format(total_profit)]
    for line in footer:
        yield line


def generate_summary(info_iter, is_generator):
    """
    A wrapper of summary.

    :param info_iter: iterable.
    :param is_generator: boolean, if the return type is a generator.
    :return: iterable, generator or list.
    """
    info_handler = info_rows_generator if is_generator else info_rows
    output_iter = info_handler(info_iter)
    for line in output_iter:
        yield line


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import doctest
    doctest.testmod()

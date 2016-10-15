#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'guti'

'''
Entry of the programme.
'''

import os
import argparse

import badminton_finance.core
import config


def load_config():
    """
    Load the configurations from config module.

    :return: dict, configurations.
    """
    config_dict = dict()
    for attr in dir(config):
        if attr.isupper():
            config_dict[attr] = getattr(config, attr)
    return config_dict

# load the configuration
_CONFIG = load_config()


def _input_from_file(is_check):
    """
    Get input from a file.
    When the file is really huge or the data format is absolutely correct, please set is_check False.

    :param is_check: boolean, if check the input each line.
    """
    with open(_CONFIG['INPUT_FILE_PATH']) as f:
        # # a simple implement if the file is a little one
        # info_list = f.readlines()
        # if is_check:
        #     map(badminton_court_cost.check_input_line, info_list)
        # return info_list

        # use generator
        for line in f:
            if is_check:
                badminton_finance.core.check_input_line(line)
            yield line


def _input_from_terminal(is_check):
    """
    Type the input in the terminal.

    :return: list, contains the input information.
    """
    input_list = list()
    while True:
        try:
            line = raw_input()
            if line in config.QUIT_FLAGS:
                break
            else:
                if is_check:
                    badminton_finance.core.check_input_line(line)
                input_list.append(line)
        except (ValueError, AssertionError), e:
                    print 'ERROR: ' + e.message
        except (EOFError, KeyboardInterrupt):
            print 'Exit the programme.'
            break
    return input_list

_INPUT_TYPE_DICT = {'file': _input_from_file, 'terminal': _input_from_terminal}


def input_summary():
    """
    Wrapper for input functions.

    :return: iterable.
    """
    input_func = _INPUT_TYPE_DICT[_CONFIG['INPUT_TYPE']]
    return input_func(_CONFIG['IS_CHECK'])


def output_summary():
    """
    Get a iterable object for output.
    When the input is a really huge one, please set the is_generator True.

    """
    info_iter = input_summary()
    if not info_iter:
        print 'Nothing for Calculation.'
        return
    # choose if using generator
    out_iter = badminton_finance.core.generate_summary(info_iter, _CONFIG['IS_GENERATOR'])
    with open(_CONFIG['OUTPUT_FILE_PATH'], 'w') as f:
        for line in out_iter:
            # print result on the screen
            if _CONFIG['IS_PRINT']:
                print line
            else:
                f.write(line + os.linesep)


def main():
    """
    Entry of this programme.
    """
    # can give some enter info
    pass

    # get options from args
    parser = argparse.ArgumentParser(prog='Badminton Finance')

    # version
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')

    # config
    parser.add_argument('-o', '--output', help='Set the output file path.')
    parser.add_argument('-i', '--input', help='Set the input file path.')
    parser.add_argument('-t', '--type', help='Choose the input type: file or terminal.', choices=('file', 'terminal'))
    parser.add_argument('-s', '--screen', help='Print the result to the screen', action='store_true')
    args = parser.parse_args()
    if args.output:
        _CONFIG['OUTPUT_FILE_PATH'] = args.output
    if args.input:
        _CONFIG['INPUT_FILE_PATH'] = args.input
    if args.type:
        _CONFIG['INPUT_TYPE'] = args.type
    if args.screen:
        _CONFIG['IS_PRINT'] = True

    # call the output function
    output_summary()

    # can give some exit info
    pass

if __name__ == '__main__':
    main()

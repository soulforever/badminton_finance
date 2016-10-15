# -*- coding: utf-8 -*-
__author__ = 'guti'

'''
Configuration of the the badminton court and oder strategy.
'''

# which way being using to input
INPUT_TYPE = 'file'

# if check each input information
IS_CHECK = True

# if using generator for the calculation
IS_GENERATOR = True

# if print the result on the screen
IS_PRINT = False

# file path if using file as input or output
INPUT_FILE_PATH = 'data/input.txt'
OUTPUT_FILE_PATH = 'data/output.txt'

# quit flags when using input_from_terminal
QUIT_FLAGS = ('q', 'quit', 'exit', 'Q', 'Quit', 'Exit', 'QUIT', 'EXIT')


def _check_config():
    """
    Check legality of the arguments in this module.

    :return: None, assert the arguments is legal.
    """
    assert_msg = 'Config file error, illegal arguments in config module'
    assert INPUT_TYPE in ('file', 'terminal'), assert_msg
    assert isinstance(IS_CHECK, bool), assert_msg
    assert isinstance(IS_GENERATOR, bool), assert_msg
    assert isinstance(IS_PRINT, bool), assert_msg

# execute when this module being imported
_check_config()

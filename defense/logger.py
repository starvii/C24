#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys


__all__ = ['get_logger']


# DEFAULT_FORMATTER = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
DEFAULT_FORMATTER = '%(asctime)s %(levelname)s %(message)s'
DEFAULT_LEVEL = logging.DEBUG


def get_logger(name, level=DEFAULT_LEVEL, formatter=DEFAULT_FORMATTER, stdout=False):
    filename = name + '.log'
    file_handler = logging.FileHandler(filename=filename, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    if stdout:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(level)
        logger.addHandler(stream_handler)
    return logger

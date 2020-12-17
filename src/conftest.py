""" conftest: global fixture file for tests """
import logging
import time

import pytest

from . import example


@pytest.fixture(autouse=True)
def time_test():
    """ Time a test and print out how long it took """
    before = time.time()
    yield
    after = time.time()
    print(f"Test took {after - before:.02f} seconds!")


@pytest.fixture(autouse=True, scope="session")
def time_all_tests():
    """ Time a test and print out how long it took """
    before = time.time()
    yield
    after = time.time()
    print(f"Total test time: {after - before:.02f} seconds!")


@pytest.fixture  # Default scope is function, default autouse is False
def logger_to_debug():
    """ Set the logger to debug """
    prev_level = example.LOGGER.getEffectiveLevel()
    example.LOGGER.setLevel(logging.DEBUG)
    yield prev_level
    example.LOGGER.setLevel(prev_level)

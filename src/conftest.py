""" conftest: global fixture file for tests """
import time

import pytest


@pytest.fixture(autouse=True)
def time_test():
    """Time a test and print out how long it took

    Note, this fixture is for example purposes. This information
    can also be achieved with the `--durations=n` command line flag.
    """
    before = time.time()
    yield
    after = time.time()
    print(f"Test took {after - before:.02f} seconds!")


@pytest.fixture(autouse=True, scope="session")
def time_all_tests():
    """ Time all tests and print out how long they took """
    before = time.time()
    yield
    after = time.time()
    print(f"Total test time: {after - before:.02f} seconds!")

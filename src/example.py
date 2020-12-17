"""example: file with example python code to pytest"""
import logging
import time

LOGGER = logging.getLogger(__name__)
GLOBAL_SLEEP_SECS = 3
DEBUG_MODE = False


class Math:
    """ Class with simple math functions to test """

    def __init__(self, multiplier=1, offset=0):
        self.multiplier = multiplier
        self.offset = offset

    def multiply(self, first, second):
        """ Multiply two numbers, with offset"""
        return first * second + self.offset

    def add(self, first, second):
        """ Add two numbers, with multiplier"""
        return (first + second) * self.multiplier

    @staticmethod
    def slow():
        """ just slow down our main function """
        print(f"SLEEPING {GLOBAL_SLEEP_SECS} seconds!")
        time.sleep(GLOBAL_SLEEP_SECS)


def some_math_function(first, second, multiplier, offset, half=False):
    """ Some function using Math """
    before = time.time()
    math = Math(multiplier, offset)
    third = math.multiply(first, second)
    math.slow()
    fourth = math.add(third, second)
    after = time.time()
    if after - before > 2:
        LOGGER.warning("warning message!")
        LOGGER.info("info message!")
        print("print message")
    if DEBUG_MODE:
        LOGGER.debug("Only in debug!")
    if half:
        fourth /= 2

    return fourth


def update_file_via_pathlib(path):
    """ Get the contents of an input pathlib file object """
    contents = path.read_text()
    new_contents = "Check this out: " + contents.strip() + " BAM!"
    path.write_text(new_contents)
    return new_contents


def error_function(raise_error):
    """ Function will raise an error if you'd like it to """
    if raise_error:
        raise RuntimeError("Alas, there is an error!")
    return True


if __name__ == "__main__":  # pragma: no cover
    # This code won't get run by tests
    print(some_math_function(1, 2, 3, 4))

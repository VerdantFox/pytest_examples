"""example: file with example python code to pytest"""
import logging
import os
import time

LOGGER = logging.getLogger(__name__)
GLOBAL_SLEEP_SECS = 3
DEBUG_MODE = False


class Math:
    """ Class with simple math functions to test """

    @staticmethod
    def add(first, second):
        """ Add two numbers"""
        return first + second

    @staticmethod
    def divide(first, second):
        """ Divide two numbers (excluding remainder)  """
        return first // second

    @staticmethod
    def multiply(first, second):
        """ Multiply two numbers"""
        return first * second

    @staticmethod
    def slow():
        """ just slow down our main function """
        print(f"SLEEPING {GLOBAL_SLEEP_SECS} seconds!")
        time.sleep(GLOBAL_SLEEP_SECS)


def some_math_function(first, second, half=False):
    """ Some function using Math """
    before = time.time()
    math = Math()
    addition = math.add(first, second)
    division = math.divide(first, second)
    math.slow()
    solution = math.multiply(addition, division)
    after = time.time()
    if after - before > 2:
        LOGGER.warning("warning message!")
        LOGGER.info("info message!")
        print("print message")
    if DEBUG_MODE:
        LOGGER.debug("Only in debug!")
    if half:
        solution /= 2

    return solution


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


def environment_var_function():
    """ Some function that deals with environment variables """
    if os.environ.get("MY_VAR") == "true":
        return "MY_VAR is set to 'true'"
    else:
        return "MY_VAR is not set to 'true'"


if __name__ == "__main__":  # pragma: no cover
    # This code won't get run by tests
    print(some_math_function(2, 1))

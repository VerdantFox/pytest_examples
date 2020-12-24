""" example_test: pytest examples using example.py """
import importlib.resources
import os
import random

import pytest

from . import example


# --------------------------------------------------
# Command args:
#    -s (show std_out even if test passes)
#    -k GLOB_NAME (run test with GLOB_NAME in name)
#    -m MARKER (run tests containing a marker)
#    -v (verbose output -- show each test's name)
#    --tb=LENGTH (adjust length of traceback messages)
#    --lf/--last-failed (re-run only the tests that failed)
# --------------------------------------------------
@pytest.mark.speed_check
def test_basic():
    """ Test main without any changes """
    answer = example.some_math_function(2, 1)
    assert answer == 6


@pytest.mark.failing
def test_failure():
    """ A test designed to fail, will raise ZeroDivisionError """
    example.Math().divide(1, 0)


# --------------------------------------------------
# Marking tests for skip or xfail
# --------------------------------------------------
@pytest.mark.skip(reason="No way of testing this properly")
def test_skipped():
    """ Mark a test to be always skipped with a reason (marked as s or SKIPPED) """
    assert False


@pytest.mark.skipif(
    os.environ.get("SKIP") != "1", reason="It only works if SKIP is set to '1'"
)
def test_skipped_if():
    """ Mark a test to be skipped under certain conditions with a reason """
    assert True


@pytest.mark.xfail(
    condition=os.environ.get("MY_VAR") == "true",
    reason="It should fail if MY_VAR is set to 'true'",
)
def test_xfail():
    """ Mark a test to be expected to fail under conditions with a reason (marked x or xfail) """
    assert example.environment_var_function() == "MY_VAR is not set to 'true'"


@pytest.mark.xfail(
    condition=os.environ.get("MY_VAR") == "true",
    reason="It should fail if MY_VAR is set to 'true' (but doesn't fail)",
)
def test_xfail_opposite():
    """ If test passes when it should fail (marked as X or xpass) """
    if os.environ.get("MY_VAR") == "true":
        assert example.environment_var_function() == "MY_VAR is set to 'true'"
    else:
        assert True


# --------------------------------------------------
# monkeypatch -- mock objects in tests and change environment
# --------------------------------------------------
# mock a global variable
@pytest.mark.speed_check
def test_faster(monkeypatch):
    """ Test with monkeypatch of slow GLOBAL_SLEEP_SECS removed """

    monkeypatch.setattr(example, "GLOBAL_SLEEP_SECS", 1)

    answer = example.some_math_function(2, 1)
    assert answer == 6


# mock a function with a lambda function
# mock a function with a replacement function
@pytest.mark.speed_check
def test_mocked_functions(monkeypatch):
    """ Test monkeypatch replacing a function with a different function """

    def fake_multiply(_self, _first, _second):
        """ Output 2 regardless of input """
        return 2

    monkeypatch.setattr(example.Math, "slow", lambda _: None)
    monkeypatch.setattr(example.Math, "multiply", fake_multiply)

    answer = example.some_math_function(2, 1)
    assert answer == 2


# set or remove an environment variable for a test
def test_alter_environment_variable(monkeypatch):
    """ Test with monkeypatch setting an environment variable """

    # If raising=True (default) will raise error if MY_VAR doesn't exist
    monkeypatch.delenv("MY_VAR", raising=False)

    assert example.environment_var_function() == "MY_VAR is not set to 'true'"

    monkeypatch.setenv("MY_VAR", "true")

    assert example.environment_var_function() == "MY_VAR is set to 'true'"


# --------------------------------------------------
# pathlib, tmp_path, and importlib stuff
# --------------------------------------------------
def test_update_file_pathlib(tmp_path):
    """ Test the update_file_pathlib function """
    # Establish path to a temporary file under a temporary directory
    test_file = tmp_path.joinpath("testfile.txt")

    # Get the file contents of a file in our test_data directory
    with importlib.resources.path(
        "pytest_examples.test_data", "infile.txt"
    ) as test_path_og:
        # Write data from our test_data directory file to the temporary file
        test_file.write_text(test_path_og.read_text())

    example.update_file_via_pathlib(test_file)
    assert test_file.read_text() == "Check this out: Awesome test data! BAM!"


# --------------------------------------------------
# Fixtures
# --------------------------------------------------
# monkeypatch and tmp_path are fixtures
#   buy you can create your own fixtures
#
# Fixtures can do something, return (or yield) information
#    and then perform more actions after yield
# In a conftest.py file (see conftest.py) or within a file
# In file:
@pytest.fixture
def speedup(monkeypatch):  # Notice I pass a fixture (monkeypatch) to another fixture
    """ Fixture to speed up tests by fixing GLOBAL_SLEEP_SECS """
    sleep_time = random.randint(1, 10) / 50
    monkeypatch.setattr(example, "GLOBAL_SLEEP_SECS", sleep_time)
    return sleep_time


def test_with_speedup(speedup):
    """ Use local fixture in test """
    answer = example.some_math_function(2, 1)
    assert answer == 6


# --------------------------------------------------
# Test code that raises errors
# --------------------------------------------------
def test_error_raising():
    """ Test that use pytest.raises to check for errors """
    with pytest.raises(RuntimeError):
        example.error_function(True)

    with pytest.raises(RuntimeError, match="Alas, there is an error!"):
        example.error_function(True)

    with pytest.raises(RuntimeError, match="Alas.*there.*error!"):
        example.error_function(True)

    assert example.error_function(False) is True


# --------------------------------------------------
# Test against captured outputs
# --------------------------------------------------
# caplog: fixture that captures log output
@pytest.mark.output_capturing
def test_caplog_standard(caplog):
    """ Use caplog to test logging messages (at standard WARNING level) """
    answer = example.some_math_function(2, 1)
    assert answer == 6
    assert "warning message!" in caplog.text
    assert "info message!" not in caplog.text


@pytest.mark.output_capturing
def test_caplog_debug(caplog, logger_to_debug):
    """Use caplog to test logging messages (at debug level)

    Note: "logger_to_debug" is custom fixture in conftest.py
    """
    answer = example.some_math_function(2, 1)
    assert answer == 6
    assert "warning message!" in caplog.text
    assert "info message!" in caplog.text


# capsys: fixture that captures sys.stdout and sys.stderr
@pytest.mark.output_capturing
def test_capsys(capsys):
    """ Use caplog to test print messages"""
    answer = example.some_math_function(2, 1)
    assert answer == 6
    captured = capsys.readouterr()  # Note this resets the internal buffer
    assert "print message" in captured.out


# --------------------------------------------------
# Parameterized testing
# run the same test under a range of conditions
# --------------------------------------------------
PARAMS = [
    (2, 1, 6),
    (7, 3, 20),
    pytest.param(25, 5, 150, id="large"),
    pytest.param(-5, -3, -8, id="with_negatives"),
]


# Simple parametrized function with params expanded
@pytest.mark.parametrization
@pytest.mark.parametrize("first, second, expected", PARAMS)
def test_param_standard(speedup, first, second, expected):
    """ Test function with standard params """
    answer = example.some_math_function(first, second)
    assert answer == expected


def param_func():
    """ Pretend this function did some dynamic thing to generate an iterable """
    dynamically_generated_iterable = (
        list(range(3, 1, -1)) + [5],
        list(range(6, 4, -1)) + [11],
    )
    return dynamically_generated_iterable


# Parametrized function with params not expanded and generated by function
@pytest.mark.parametrization
@pytest.mark.parametrize("params", param_func())
def test_param_function(speedup, params):
    """ Test function with standard params """
    answer = example.some_math_function(params[0], params[1])
    assert answer == params[2]


# Multiple sets of parameters in conjunction
@pytest.mark.parametrization
@pytest.mark.parametrize("first, second, expected", PARAMS)
@pytest.mark.parametrize("half", (True, False))
def test_param_multiple_sets(speedup, first, second, expected, half):
    """ Test 2 sets of parameters """
    answer = example.some_math_function(first, second, half=half)
    if half:
        assert answer == expected / 2
    else:
        assert answer == expected


# --------------------------------------------------
# pytest-cov (coverage.py)
# --------------------------------------------------
#
# examples:
# pytest --cov=src
# pytest --cov=src --cov-report=html
#
# comment "# pragma: no cover" to ignore a line or code block from coverage

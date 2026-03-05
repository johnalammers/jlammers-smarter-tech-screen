import pytest

import sorter
from sorter import sort
from sorter import PackageStack

# Test Notes
#
# Parameterized tests vs. test functions.
# With the ability to specify the expected return value and a human-readable test ID,
# one *could* have a single, heavily parameterized test function.
# That would be fine, functionally, but from a test development and developer
# experience perspective, especially if you're doing TDD, I still like having separate
# functions for different test scenarios. I tend to use parameterization to fight
# combinatorial explosion of test functions, not because I love them from an ergonomic
# perspective.
#
# Literal values in tests
# While I go to great lengths to avoid literal values in production code, I tend to
# use literals in test code if/where I think they aid readability. Sometimes avoiding
# literals can result in overly abstract tests, and you want your tests as simple to
# read as possible. Here I've added constants for dimensions and mass I use over and
# over for edge testing. I've not, however, added constants for testing the volume
# check, because it would hurt readability since it's a contrived set of interrelated
# values.

SAFE_DIMENSION = 10  # Cannot produce a volume violation without a dimension violation in another parameter
INSIDE_BULKY_DIMENSION_EDGE = sorter.BULKY_DIMENSION - 0.1
INSIDE_HEAVY_EDGE = sorter.HEAVY_MASS - 0.1


def test_if_neither_bulky_nor_heavy_put_on_normal_stack_happy_path():
    stack = sort(SAFE_DIMENSION, SAFE_DIMENSION, SAFE_DIMENSION, INSIDE_HEAVY_EDGE)
    assert stack == PackageStack.STANDARD.value


@pytest.mark.parametrize("width, height, length", [
    pytest.param(INSIDE_BULKY_DIMENSION_EDGE, SAFE_DIMENSION, SAFE_DIMENSION, id="Width edge test"),
    pytest.param(SAFE_DIMENSION, INSIDE_BULKY_DIMENSION_EDGE, SAFE_DIMENSION, id="Height edge test"),
    pytest.param(SAFE_DIMENSION, SAFE_DIMENSION, INSIDE_BULKY_DIMENSION_EDGE, id="Length edge test"),
])
def test_if_neither_bulky_nor_heavy_put_on_normal_stack_edge_cases(width: float, height: float, length: float):
    stack = sort(width, height, length, INSIDE_HEAVY_EDGE)
    assert stack == PackageStack.STANDARD.value


@pytest.mark.parametrize("width, height, length", [
    pytest.param(sorter.BULKY_DIMENSION, SAFE_DIMENSION, SAFE_DIMENSION, id="Too wide"),
    pytest.param(SAFE_DIMENSION, sorter.BULKY_DIMENSION, SAFE_DIMENSION, id="Too high"),
    pytest.param(SAFE_DIMENSION, SAFE_DIMENSION, sorter.BULKY_DIMENSION, id="Too long")
])
def test_if_bulky_by_dimension_but_not_heavy_put_on_special_stack(width: float, height: float, length: float):
    stack = sort(width, height, length, INSIDE_HEAVY_EDGE)
    assert stack == PackageStack.SPECIAL.value


def test_if_bulky_by_volume_but_not_heavy_put_on_special_stack():
    stack = sort(100, 100, 100, 5)
    assert stack == PackageStack.SPECIAL.value


def test_if_heavy_put_on_special_stack():
    stack = sort(SAFE_DIMENSION, SAFE_DIMENSION, SAFE_DIMENSION, sorter.HEAVY_MASS)
    assert stack == PackageStack.SPECIAL.value


# Invalid dimensions or mass
# This wasn't in the spec, because it should be impossible, but
# we should account for it anyway. Hardware malfunctions of bugs
# in the calling software could result in nonsensical values.
@pytest.mark.parametrize("width, height, length, mass", [
    (0, 1, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
    (-1, 1, 1, 1),
    (1, -1, 1, 1),
    (1, 1, -1, 1),
    (1, 1, 1, -1),
])
def test_invalid_dimension_or_mass_put_on_rejected_stack(width: float, height: float, length: float, mass: float):
    with pytest.raises(ValueError):
        sort(width, height, length, mass)


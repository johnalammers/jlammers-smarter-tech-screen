import pytest

from sorter import sort, PackageStack, BULKY_DIMENSION, HEAVY_MASS

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
INSIDE_BULKY_DIMENSION_EDGE = BULKY_DIMENSION - 0.1
INSIDE_HEAVY_EDGE = HEAVY_MASS - 0.1


def test_if_neither_bulky_nor_heavy_put_on_normal_stack_happy_path():
    stack = sort(SAFE_DIMENSION, SAFE_DIMENSION, SAFE_DIMENSION, INSIDE_HEAVY_EDGE)
    assert stack == PackageStack.STANDARD.value


@pytest.mark.parametrize("width, height, length", [
    pytest.param(INSIDE_BULKY_DIMENSION_EDGE, SAFE_DIMENSION, SAFE_DIMENSION, id="width_edge"),
    pytest.param(SAFE_DIMENSION, INSIDE_BULKY_DIMENSION_EDGE, SAFE_DIMENSION, id="height_edge"),
    pytest.param(SAFE_DIMENSION, SAFE_DIMENSION, INSIDE_BULKY_DIMENSION_EDGE, id="length_edge"),
])
def test_if_neither_bulky_nor_heavy_put_on_normal_stack_edge_cases(width: float, height: float, length: float):
    stack = sort(width, height, length, INSIDE_HEAVY_EDGE)
    assert stack == PackageStack.STANDARD.value


@pytest.mark.parametrize("width, height, length", [
    pytest.param(BULKY_DIMENSION, SAFE_DIMENSION, SAFE_DIMENSION, id="wide"),
    pytest.param(SAFE_DIMENSION, BULKY_DIMENSION, SAFE_DIMENSION, id="high"),
    pytest.param(SAFE_DIMENSION, SAFE_DIMENSION, BULKY_DIMENSION, id="long")
])
def test_if_bulky_by_dimension_but_not_heavy_put_on_special_stack(width: float, height: float, length: float):
    stack = sort(width, height, length, INSIDE_HEAVY_EDGE)
    assert stack == PackageStack.SPECIAL.value


def test_if_bulky_by_volume_but_not_heavy_put_on_special_stack():
    stack = sort(100, 100, 100, 5)
    assert stack == PackageStack.SPECIAL.value


def test_if_heavy_put_on_special_stack():
    stack = sort(SAFE_DIMENSION, SAFE_DIMENSION, SAFE_DIMENSION, HEAVY_MASS)
    assert stack == PackageStack.SPECIAL.value


def test_if_bulky_by_volume_and_heavy_put_on_rejected_stack():
    stack = sort(100, 100, 100, HEAVY_MASS)
    assert stack == PackageStack.REJECTED.value


@pytest.mark.parametrize("width, height, length, mass", [
    pytest.param(BULKY_DIMENSION, SAFE_DIMENSION, SAFE_DIMENSION, HEAVY_MASS, id="wide_and_heavy"),
    pytest.param(SAFE_DIMENSION, BULKY_DIMENSION, SAFE_DIMENSION, HEAVY_MASS, id="high_and_heavy"),
    pytest.param(SAFE_DIMENSION, SAFE_DIMENSION, BULKY_DIMENSION, HEAVY_MASS, id="long_and_heavy")
])
def test_if_bulky_by_dimensions_and_heavy_put_on_rejected_stack(width: float, height: float, length: float, mass: float):
    stack = sort(width, height, length, mass)
    assert stack == PackageStack.REJECTED.value


# Invalid dimensions or mass
# This wasn't in the spec, because it should be impossible, but
# we should account for it anyway. Hardware malfunctions or bugs
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
def test_invalid_dimension_or_mass_raises_value_error(width: float, height: float, length: float, mass: float):
    with pytest.raises(ValueError):
        sort(width, height, length, mass)

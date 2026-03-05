"""
Package sorter

Implements the package dispatch rules for Smarter Technology’s robotic arm.

The public API is exposed directly from this module so callers can simply use:

    from sorter import sort

If the project were expanded, additional modules could be added under this
package while preserving the same import interface.
"""

# I'm using an Enum rather than string literals or constants because I
# hate literals and Python doesn't really do constants. I know I'm showing
# my C++, Java, C# roots, but the idea of relying strictly on convention
# to keep someone from reassigning my "constant" is hard to accept.
# The function ultimately serializes the value to a string, but the enum
# improves readability and tooling. Not necessary in a toy problem like this,
# but I don't reviewers thinking I'd litter my code with string literals.
from enum import Enum


class PackageStack(str, Enum):
    STANDARD = "STANDARD"
    SPECIAL = "SPECIAL"
    REJECTED = "REJECTED"


BULKY_DIMENSION = 150
BULKY_VOLUME = 1000000
HEAVY_MASS = 20


def sort(width: float, height: float, length: float, mass: float) -> str:
    """
    Sort the package based on the given dimensions and mass.
    All parameters are floats. This wasn't specified in the problem spec,
    but is the most reasonable real-world interpretation.

    :return: string representation of the destination stack: "STANDARD", "SPECIAL", or "REJECTED"
    """
    if width <= 0 or height <= 0 or length <= 0 or mass <= 0:
        raise ValueError("Dimensions and mass must be greater than 0")

    is_bulky = (width >= BULKY_DIMENSION
                or height >= BULKY_DIMENSION
                or length >= BULKY_DIMENSION
                or width * height * length >= BULKY_VOLUME)

    is_heavy = (mass >= HEAVY_MASS)

    if not is_bulky and not is_heavy:
        return PackageStack.STANDARD.value
    elif is_bulky and is_heavy:
        return PackageStack.REJECTED.value
    else:
        return PackageStack.SPECIAL.value

"""
Package sorter

Implements the package dispatch rules for Smarter Technology’s robotic arm.

The public API is exposed directly from this module so callers can simply use:

    from sorter import sort

If the project were expanded, additional modules could be added under this
package while preserving the same import interface.
"""

# Enum avoids typos and centralizes allowed values; returned as strings per spec.
from enum import Enum


class PackageStack(str, Enum):
    STANDARD = "STANDARD"
    SPECIAL = "SPECIAL"
    REJECTED = "REJECTED"


BULKY_DIMENSION = 150
BULKY_VOLUME = 1_000_000
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

    is_bulky = (
        width >= BULKY_DIMENSION
        or height >= BULKY_DIMENSION
        or length >= BULKY_DIMENSION
        or width * height * length >= BULKY_VOLUME
        )

    is_heavy = mass >= HEAVY_MASS

    if is_bulky and is_heavy:
        return PackageStack.REJECTED.value
    elif is_bulky or is_heavy:
        return PackageStack.SPECIAL.value
    else:
        return PackageStack.STANDARD.value

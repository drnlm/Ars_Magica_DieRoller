"""A AM5 simple die roll"""

from .utils import die_roller


def simple_roll(modifier):
    """Roll a simple die"""
    roll = die_roller()
    if roll == 0:
        result = 10
    else:
        result = roll
    return [roll], result + modifier, ''

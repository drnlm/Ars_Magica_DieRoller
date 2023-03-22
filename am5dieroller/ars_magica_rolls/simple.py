"""A AM5 simple die roll"""

from .utils import die_roller


def simple_roll(modifier):
    """Roll a simple die"""
    roll = die_roller()
    return [roll], roll + modifier, ''

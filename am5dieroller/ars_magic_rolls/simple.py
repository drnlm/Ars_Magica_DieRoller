from .utils import die_roller


def simple_roll(modifier):
    roll = die_roller()
    return [roll], roll + modifier, ''

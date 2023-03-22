"""Handle botch rolls"""

from .utils import die_roller

def botch_roll(number):
    """Roll the given number of botch dice and report the result"""
    rolls  = [die_roller() for x in range(number)]
    botches = rolls.count(0)
    if botches > 0:
        outcome = 'botched'
    else:
        outcome = 'no botch'
    return rolls, botches, outcome

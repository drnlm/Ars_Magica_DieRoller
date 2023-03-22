"""Handle stessed die rolls"""

from .utils import die_roller


def stressed_die():
    """Implement a stressed die with open-end rerolls"""
    done = False
    multiplier = 1
    rolls = []
    total = 0
    while not done:
        this_roll = die_roller()
        if this_roll != 1:
            if rolls and this_roll == 0:
                this_roll = 10
            done = True
            total = multiplier * this_roll
        else:
            multiplier *= 2
            if len(rolls) >= 20:
                # We're in ludicrious terrory, so we bail out already
                total = multiplier
                done = True
        rolls.append(this_roll)
    return rolls, total



def stressed_roll(modifier):
    """Roll a stressed die and return results and outcomes"""
    rolls, total = stressed_die()
    if rolls[0] == 0:
        outcome = 'possible botch'
    elif rolls[0] == 1:
        outcome = 'open-end'
    else:
        outcome = ''

    return rolls, total + modifier, outcome

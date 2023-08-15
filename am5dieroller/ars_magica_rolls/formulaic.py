"""Handle formulaic spell rolls"""

from .stressed import stressed_die
from .utils import die_roller


def formulaic_roll(modifier, target):
    """Cast a formulaic spell using a stressed die.

       Return the result (success, success with fatigure, failure)
       and possible botches"""
    rolls, total = stressed_die()
    result = total + modifier
    if result >= target:
        if rolls[0] == 0:
            outcome = "possible success"
        else:
            outcome = "success"
    elif target - result <= 10:
        if rolls[0] == 0:
            outcome = "possible success (with fatigue)"
        else:
            outcome = "success (with fatigue)"
    else:
        outcome = "failure (with fatigue)"
    if rolls[0] == 0:
        outcome += ' (possible botch)'
    return rolls, result, outcome



def formulaic_simple_roll(modifier, target):
    """Cast a formulaic spell using a simple die.

       Return the result (success, success with fatigue, failure)"""
    roll = die_roller()
    result = roll + modifier
    if roll == 0:
        result += 10
    if result >= target:
        outcome = "success"
    elif target - result <= 10:
        outcome = "success (with fatigue)"
    else:
        outcome = "failure (with fatigue)"
    return [roll], result, outcome


def ritual_roll(modifier, target):
    """Cast a ritual spell using a stressed die.

       Return the result (success with fatigue (varying levels), failure)
       and possible botches"""
    rolls, total = stressed_die()
    result = total + modifier
    if result >= target - 10:
        if rolls[0] == 0:
            outcome = "possible success"
        else:
            outcome = "success"
    else:
        outcome = "failure"
    if result >= target:
        outcome += " (1 fatigue level)"
    elif result >= target - 5:
        outcome += " (2 fatigue levels)"
    elif result >= target - 10:
        outcome += " (3 fatigue levels)"
    elif result >= target - 15:
        outcome += " (4 fatigue levels)"
    else:
        outcome += " (5 fatigue levels)"
    if rolls[0] == 0:
        outcome += ' (possible botch)'
    return rolls, result, outcome

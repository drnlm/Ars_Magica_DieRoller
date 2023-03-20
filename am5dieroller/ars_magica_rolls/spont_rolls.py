from .stressed import stressed_die

def spont_roll(modifier, target):
    roll = 0

    result = (0 + modifier) // 5
    if result >= target:
        outcome = "success"
    else:
        outcome = "failure"
    return roll, roll + modifier, result, outcome


def fatiguing_spont_roll(modifier, target):
    rolls, total = stressed_die()
    result = (total + modifier) // 2
    if result >= target:
        if rolls[0] == 0:
            outcome = "possible success"
        else:
            outcome = "success"
    else:
        outcome = "failure"
    if rolls[0] == 0:
        outcome += ' (possible botch)'
    return rolls, total + modifier, result, outcome

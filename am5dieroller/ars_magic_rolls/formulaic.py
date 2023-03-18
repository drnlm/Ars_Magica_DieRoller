from .stressed import stressed_die


def formulaic_roll(modifier, target):
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

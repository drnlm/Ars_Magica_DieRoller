# Internal helpers from 

from am5dieroller.ars_magica_rolls.stressed import stressed_roll
from am5dieroller.ars_magica_rolls.formulaic import formulaic_roll, formulaic_simple_roll, ritual_roll
from am5dieroller.ars_magica_rolls.spont_rolls import spont_non_roll, fatiguing_spont_roll
from am5dieroller.ars_magica_rolls.simple import simple_roll
from am5dieroller.ars_magica_rolls.botch import botch_roll


# Internal formating helpers, to make aliases and testing easier

# It's non-trivial to create aliases without repeating boilerplate,
# so this separation minimises the repeated code and similifies
# testing


def stressed_internal(modifier):
    """Format a stressed die result"""
    rolls, total, outcome = stressed_roll(modifier)
    if len(rolls) > 1:
        result = f'Rolls: {rolls}. Total (with modifier {modifier}): **{total}**'
    else:
        result = f'Roll: {rolls[0]}. Total (with modifier {modifier}): **{total}**'
    if outcome:
        result += f'\n**{outcome}**\n'
    return result


def simple_internal(modifier):
    """Format a simple die result"""
    rolls, total, _ = simple_roll(modifier)
    result = f'Roll: {rolls[0]}. Total (with modifier {modifier}): **{total}**'
    return result


def botch_internal(number):
    """Format a botch roll result"""
    rolls, botches, outcome = botch_roll(number)
    if number > 1:
        result = f'Rolls: {rolls}. Botches: **{botches}**  --  **{outcome}**'
    else:
        result = f'Roll: **{rolls[0]}**  --  **{outcome}**'
    return result


def formulaic_ritual_internal(casting_score, target, roll_function):
    """Format a stressed formulaic spell roll result"""
    rolls, total, outcome = roll_function(casting_score, target)
    if len(rolls) > 1:
        result = f'Rolls: {rolls}. Total (with casting score {casting_score}): **{total}** (against {target})'
    else:
        result = f'Roll: {rolls[0]}. Total (with casting score {casting_score}): **{total}** (against {target})'
    result += f'\n**{outcome}**\n'
    return result


def formulaic_simple_internal(casting_score, target):
    """Format a simple formulaic spell roll result"""
    rolls, total, outcome = formulaic_simple_roll(casting_score, target)
    result = f'Roll: {rolls[0]}. Total (with casting score {casting_score}): **{total}** (against {target})'
    result += f'\n**{outcome}**\n'
    return result


def spontaneous_internal(casting_score, target):
    """Format a spontaneous spell result"""
    _, total, modified_total, outcome = spont_non_roll(casting_score, target)
    result = f'Total: {total}. Final total: **{modified_total}** (against {target})'
    result += f'\n**{outcome}**\n'
    return result


def fspont_internal(casting_score, target):
    """Format a fatiguing spontaneous spell roll result"""
    rolls, total, modified_total, outcome = fatiguing_spont_roll(casting_score, target)
    if len(rolls) > 1:
        result = f'Rolls: {rolls}. Total (with casting score {casting_score}): {total}. Final total: **{modified_total}** (against {target})'
    else:
        result = f'Roll: {rolls[0]}. Total (with casting score {casting_score}): {total}. Final total: **{modified_total}** (against {target})'
    result += f'\n**{outcome}**\n'
    return result


def ritual_internal(casting_score, target):
    """Wrapper to call formulaic_ritual_internal with the ritual roller"""
    return formulaic_ritual_internal(casting_score, target, ritual_roll)


def formulaic_internal(casting_score, target):
    """Wrapper to call formulaic_ritual_internal with the formulaic roller"""
    return formulaic_ritual_internal(casting_score, target, formulaic_roll)

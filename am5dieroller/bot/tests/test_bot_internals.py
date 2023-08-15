"""This tests the internal functions to make sure we're basically calling the right thing
and formatting the results correctly

We don't try to mock out the actual discord API, relying on the discord.py people
to handle that testing"""

from unittest.mock import Mock, patch

from ..internal import (stressed_internal, simple_internal, botch_internal,
                        formulaic_internal, formulaic_simple_internal,
                        spontaneous_internal, fspont_internal,
                        ritual_internal)


def test_botch_no_botch():
    """Check that a single roll with no botch reports correctly"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = botch_internal(1)
        assert 'Roll:' in result
        assert '**no botch**' in result


def test_botch_botch_multiple():
    """Check that multiple rolls with a botch reports correctly"""
    with patch('random.randint', new_callable=Mock, side_effect=[6, 0]):
        result = botch_internal(2)
        assert 'Rolls:' in result
        assert '**botched**' in result


def test_simple_non_zero():
    """Check simple die non-zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = simple_internal(5)
        assert '**11**' in result
        assert 'Roll: 6.' in result


def test_simple_zero():
    """Check simple die with 0 roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        result = simple_internal(5)
        assert '**15**' in result
        assert 'botch' not in result
        assert 'Roll: 10 (0 on d10).' in result


def test_stressed_non_zero():
    """Check stressed die non-zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = stressed_internal(5)
        assert '**11**' in result
        assert 'Roll: 6.' in result


def test_stressed_open_end():
    """Check stressed die open-emded roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 6]):
        result = stressed_internal(5)
        assert '**17**' in result
        assert 'Rolls: [1, 6].' in result
        assert '**open-end**' in result


def test_stressed_zero():
    """Check stressed die with 0 roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        result = stressed_internal(5)
        assert '**5**' in result
        assert 'Roll: 0.' in result
        assert '**possible botch**' in result


def test_spont_failure():
    """Test a spontaneous casting non-roll"""
    result = spontaneous_internal(5, 25)
    assert '**1** (against 25)' in result
    assert '**failure**' in result


def test_spont_success():
    """Test a spontaneous casting non-roll"""
    result = spontaneous_internal(25, 5)
    assert '**5** (against 5)' in result
    assert '**success**' in result


def test_fspont_non_zero_failure():
    """Test a fatiguing spontaneous casting roll failing"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = fspont_internal(5, 25)
        assert '**failure**' in result
        assert 'Roll: 6' in result
        assert ' Final total: **5**' in result


def test_fspont_non_zero_success():
    """Test a fatiguing spontaneous casting roll succeeding"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = fspont_internal(16, 10)
        assert '**success**' in result
        assert 'Roll: 6' in result
        assert ' Final total: **11**' in result


def test_fspont_open_end():
    """Test a fatiguing spontaneous casting roll open-ending"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 6]):
        result = fspont_internal(10, 10)
        assert '**success**' in result
        assert 'Rolls: [1, 6]' in result
        assert ' Final total: **11**' in result


def test_fspont_zero():
    """Test a fatiguing spontaneous casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        result = fspont_internal(5, 25)
        assert '**failure (possible botch)**' in result
        assert 'Roll: 0' in result
        assert 'Final total: **2**' in result


def test_formulaic_non_zero_failure():
    """Test a formulaic casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_internal(5, 25)
        assert '**failure (with fatigue)**' in result
        assert 'Roll: 6' in result
        assert  '**11**' in result


def test_formulaic_non_zero_sucess_with_fatigue():
    """Test a formulaic casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_internal(5, 15)
        assert '**success (with fatigue)**' in result
        assert 'Roll: 6' in result
        assert '**11**' in result


def test_formulaic_non_zero_sucess_with_no_fatigue():
    """Test a formulaic casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_internal(20, 25)
        assert '**success**' in result
        assert 'Roll: 6' in result
        assert '**26**' in result


def test_formulaic_open_end():
    """Test a formulaic casting roll open-ending"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 6]):
        result = formulaic_internal(16, 25)
        assert '**success**' in result
        assert 'Rolls: [1, 6]' in result
        assert '**28**' in result


def test_formulaic_zero():
    """Test a formulaic casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        result = formulaic_internal(5, 25)
        assert 'Roll: 0' in result
        assert '**failure (with fatigue) (possible botch)**' in result
        assert '**5**' in result


def test_formulaic_simple_non_zero_failure():
    """Test a formulaic simple casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_simple_internal(5, 25)
        assert 'Roll: 6' in result
        assert '**11**' in result
        assert '**failure (with fatigue)**' in result


def test_formulaic_simple_non_zero_success_fatigue():
    """Test a formulaic simple casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_simple_internal(15, 25)
        assert 'Roll: 6' in result
        assert '**21**' in result
        assert '**success (with fatigue)**' in result


def test_formulaic_simple_non_zero_success_no_fatigue():
    """Test a formulaic simple casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_simple_internal(20, 25)
        assert 'Roll: 6' in result
        assert '**26**' in result
        assert '**success**' in result


def test_formulaic_simple_zero():
    """Test a formulaic simple casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        result = formulaic_simple_internal(5, 20)
        assert 'Roll: 10 (0 on d10).' in result
        assert '**15**' in result
        assert '**success (with fatigue)**' in result
        assert '**possible botch**' not in result


def test_ritual_non_zero():
    """Test a ritual casting roll succeeding"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = ritual_internal(25, 15)
        assert 'Roll: 6' in result
        assert '**31**' in result
        assert '**success (1 fatigue level)**' in result


def test_ritual_open_end():
    """Test a ritual casting roll open-ending"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 6]):
        result = ritual_internal(10, 25)
        assert 'Rolls: [1, 6]' in result
        assert '**22**' in result
        assert '**success (2 fatigue levels)**' in result


def test_ritual_zero():
    """Test a ritual casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        result = ritual_internal(5, 25)
        assert 'Roll: 0' in result
        assert '**5**' in result
        assert '*failure (5 fatigue levels) (possible botch)**' in result


def test_ritual_narrow_fail():
    """Test a ritual casting roll with a 4 fatigue failue"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = ritual_internal(8, 25)
        assert 'Roll: 6' in result
        assert '**14**' in result
        assert '**failure (4 fatigue levels)**' in result


def test_ritual_narrow_success():
    """Test a ritual casting roll with a 3 fatigue success"""
    with patch('random.randint', new_callable=Mock, side_effect=[7]):
        result = ritual_internal(5, 20)
        assert 'Roll: 7' in result
        assert '**12**' in result
        assert '**success (3 fatigue levels)**' in result

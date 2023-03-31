# This tests the internal functions to make sure we're basically calling the right thing
# We don't try to mock out the actual discord API, relying on the discord.py people
# to handle that testing

from unittest.mock import Mock, patch

from ..internal import (stressed_internal, simple_internal, botch_internal,
                        formulaic_internal, formulaic_simple_internal,
                        spontaneous_internal, fspont_internal, formulaic_internal,
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
        assert '**5**' in result
        assert 'botch' not in result
        assert 'Roll: 0.' in result


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
    assert '**possible botch**' in result


def test_spont_success():
    """Test a spontaneous casting non-roll"""
    result = spontaneous_internal(5, 25)
    assert '**possible botch**' in result


def test_fspont_non_zero():
    """Test a fatiguing spontaneous casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = fspont_internal(5, 25)
        assert '**possible botch**' in result


def test_fspont_open_end():
    """Test a fatiguing spontaneous casting roll open-ending"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = fspont_internal(5, 25)
        assert '**possible botch**' in result


def test_fspont_zero():
    """Test a fatiguing spontaneous casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = fspont_internal(5, 25)
        assert '**possible botch**' in result


def test_formulaic_non_zero():
    """Test a formulaic casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_internal(5, 25)
        assert '**possible botch**' in result


def test_formulaic_open_end():
    """Test a formulaic casting roll open-ending"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_internal(5, 25)
        assert '**possible botch**' in result


def test_formulaic_zero():
    """Test a formulaic casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_internal(5, 25)
        assert '**possible botch**' in result


def test_formulaic_simple_non_zero():
    """Test a formulaic simple casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_simple_internal(5, 25)
        assert '**possible botch**' in result


def test_formulaic_simple_zero():
    """Test a formulaic simple casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = formulaic_simple_internal(5, 25)
        assert '**possible botch**' in result


def test_ritual_non_zero():
    """Test a ritual casting roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = ritual_internal(5, 25)
        assert '**possible botch**' in result


def test_ritual_open_end():
    """Test a ritual casting roll open-ending"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = ritual_internal(5, 25)
        assert '**possible botch**' in result


def test_ritual_zero():
    """Test a ritual casting roll with a zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        result = ritual_internal(5, 25)
        assert '**possible botch**' in result




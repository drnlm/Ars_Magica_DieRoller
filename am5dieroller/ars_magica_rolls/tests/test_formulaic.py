"""Tests for formulaic spell rolls"""

from unittest.mock import Mock, patch

from ..formulaic import formulaic_roll, formulaic_simple_roll


def test_formulaic_success():
    """Test that a formulaic spell can succeed if greater than the target"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        # 31 > 5
        _rolls, total, outcome = formulaic_roll(25, 5)
        assert total == 31
        assert outcome == 'success'
        assert 'fatigue' not in outcome


def test_formulaic_fatguing_success():
    """Test that a formulaic can succeed if wihtin 10 of the target"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        # 11 < 15, but with range
        _rolls, total, outcome = formulaic_roll(5, 15)
        assert total == 11
        assert outcome == 'success (with fatigue)'


def test_formulaic_zero_success_margin():
    """Test that a formulaic spell succeeds without fatigue if we exactly make the level"""
    with patch('random.randint', new_callable=Mock, side_effect=[5]):
        _rolls, total, outcome = formulaic_roll(5, 10)
        assert total == 10
        assert outcome == 'success'
        assert 'fatigue' not in outcome


def test_formulaic_neg_1_margin():
    """Test that a formulaic spell succeeds with fatigue if we just miss"""
    with patch('random.randint', new_callable=Mock, side_effect=[4]):
        _rolls, total, outcome = formulaic_roll(5, 10)
        assert total == 9
        assert outcome == 'success (with fatigue)'


def test_formulaic_neg_10_margin():
    """Test that a formulaic spell succeeds with fatigue if are at -10"""
    with patch('random.randint', new_callable=Mock, side_effect=[5]):
        _rolls, total, outcome = formulaic_roll(5, 20)
        assert total == 10
        assert outcome == 'success (with fatigue)'


def test_formulaic_neg_11_margin():
    """Test that a formulaic spell fails if we just miss the -10 margin"""
    with patch('random.randint', new_callable=Mock, side_effect=[4]):
        _rolls, total, outcome = formulaic_roll(5, 20)
        assert total == 9
        assert outcome == 'failure (with fatigue)'


def test_formulaic_fail():
    """Test that a formulaic spell can fail"""
    with patch('random.randint', new_callable=Mock, side_effect=[2]):
        # 7 < 35
        _rolls, total, outcome = formulaic_roll(5, 35)
        assert total == 7
        assert outcome == 'failure (with fatigue)'


def test_formulaic_possible_botch_or_success():
    """Test that a formulaic spell can detect a possible botch which would succeed if 0"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        _rolls, total, outcome = formulaic_roll(25, 5)
        assert total == 25
        assert 'possible success' in outcome
        assert 'fatigue' not in outcome
        assert 'possible botch' in outcome


def test_formulaic_possible_botch_or_fatiguing_success():
    """Test that a formulaic spell can detect a possible botch which would succeed
       with fatigue if 0"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        _rolls, total, outcome = formulaic_roll(5, 10)
        assert total == 5
        assert 'possible success (with fatigue)' in outcome
        assert 'possible botch' in outcome


def test_formulaic_possible_botch_or_failure():
    """Test that a formulaic spell can detect a possible botch on failure"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        _rolls, total, outcome = formulaic_roll(5, 25)
        assert total == 5
        assert 'failure (with fatigue)' in outcome
        assert 'possible botch' in outcome


def test_formulaic_openend_success():
    """Test that a formulaic spell can open-end and succeed"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 6]):
        rolls, total, outcome = formulaic_roll(25, 15)
        assert len(rolls) == 3
        assert total == 49
        assert 'success' in outcome
        assert 'fatigue' not in outcome


def test_formulaic_openend_fatiguing_success():
    """Test that a formulaic spell can open-end with a fatiguing success"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 6]):
        rolls, total, outcome = formulaic_roll(5, 35)
        assert len(rolls) == 3
        assert total == 29
        assert 'success (with fatigue)' in outcome


def test_formulaic_openend_failure():
    """Test that a formulaic spell can open-end with a failure result"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 2]):
        rolls, total, outcome = formulaic_roll(5, 55)
        assert len(rolls) == 3
        assert total == 13
        assert 'failure (with fatigue)' in outcome


def test_formulaic_simple_success():
    """Test that a formulaic spell can succeed if greater than the target"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        # 31 > 5
        _rolls, total, outcome = formulaic_simple_roll(25, 5)
        assert total == 31
        assert outcome == 'success'


def test_formulaic_simple_fatguing_success():
    """Test that a formulaic can succeed if wihtin 10 of the target"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        # 11 < 15, but with range
        _rolls, total, outcome = formulaic_simple_roll(5, 15)
        assert total == 11
        assert outcome == 'success (with fatigue)'


def test_formulaic_simple_zero_success_margin():
    """Test that a formulaic spell succeeds without fatigue if we exactly make the level"""
    with patch('random.randint', new_callable=Mock, side_effect=[5]):
        _rolls, total, outcome = formulaic_simple_roll(5, 10)
        assert total == 10
        assert outcome == 'success'
        assert 'fatigue' not in outcome


def test_formulaic_simple_neg_1_margin():
    """Test that a formulaic spell succeeds with fatigue if we just miss"""
    with patch('random.randint', new_callable=Mock, side_effect=[4]):
        _rolls, total, outcome = formulaic_simple_roll(5, 10)
        assert total == 9
        assert outcome == 'success (with fatigue)'


def test_formulaic_simple_neg_10_margin():
    """Test that a formulaic spell succeeds with fatigue if are at -10"""
    with patch('random.randint', new_callable=Mock, side_effect=[5]):
        _rolls, total, outcome = formulaic_simple_roll(5, 20)
        assert total == 10
        assert outcome == 'success (with fatigue)'


def test_formulaic_simple_neg_11_margin():
    """Test that a formulaic spell fails if we just miss the -10 margin"""
    with patch('random.randint', new_callable=Mock, side_effect=[4]):
        _rolls, total, outcome = formulaic_simple_roll(5, 20)
        assert total == 9
        assert outcome == 'failure (with fatigue)'


def test_formulaic_simple_fail():
    """Test that a formulaic spell can fail"""
    with patch('random.randint', new_callable=Mock, side_effect=[2]):
        # 7 < 35
        _rolls, total, outcome = formulaic_simple_roll(5, 35)
        assert total == 7
        assert outcome == 'failure (with fatigue)'


def test_formulaic_simple_no_botch():
    """Test that a formulaic spell with a simple roll doesn't botch on 0"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        _rolls, total, outcome = formulaic_simple_roll(25, 5)
        assert total == 25
        assert outcome == 'success'

# Tests for stressed die rolls

from unittest.mock import Mock, patch

from ..stressed import stressed_die, stressed_roll


def test_stressed_die_normal():
    """Test that we get the expected result for a non-open-end, non-zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        rolls, total = stressed_die()
        assert len(rolls) == 1
        assert total == 6


def test_stressed_die_open_end_once():
    """Test that an open-end works as expected"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 6]):
        rolls, total = stressed_die()
        assert len(rolls) == 2
        assert total == 12


def test_stressed_die_open_end_once_ten():
    """Test that 0's are treated as tens in an open-end"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 0]):
        rolls, total = stressed_die()
        assert len(rolls) == 2
        assert total == 20


def test_stressed_die_open_end_five():
    """Test that a long open-end works as expected"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 1, 1, 1, 3]):
        rolls, total = stressed_die()
        assert len(rolls) == 6
        assert total == 96


def test_stressed_die_open_end_four_ten():
    """Test that 0's are treated as tens in an long open-end"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 1, 1, 0]):
        rolls, total = stressed_die()
        assert len(rolls) == 5
        assert total == 160


def test_stressed_die_open_end_infinity():
    """Test that the insane run catching works"""
    with patch('random.randint', new_callable=Mock, side_effect=[1]*30):
        rolls, total = stressed_die()
        assert len(rolls) == 21
        assert total == 2097152


def test_stressed_die_zero():
    """Test that we get the expected result on a zero"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        rolls, total = stressed_die()
        assert len(rolls) == 1
        assert rolls[0] == 0
        assert total == 0


def test_stressed_roll_normal():
    """Test that normal rolls works"""
    with patch('random.randint', new_callable=Mock, side_effect=[5]):
        rolls, total, outcome = stressed_roll(10)
        assert len(rolls) == 1
        assert total == 15
        assert outcome == ''


def test_stressed_roll_open_end():
    """Test that open-end rolls work"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 5]):
        rolls, total, outcome = stressed_roll(10)
        assert len(rolls) == 3
        assert total == 30
        assert outcome == 'open-end'


def test_stressed_roll_open_end_ten():
    """Test that open-end rolls work with 0's treated as 10s"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 0]):
        rolls, total, outcome = stressed_roll(10)
        assert len(rolls) == 3
        assert total == 50
        assert outcome == 'open-end'


def test_stressed_roll_possible_botch():
    """Test that the stressed roll reports a possible botch correctly"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        rolls, total, outcome = stressed_roll(10)
        assert len(rolls) == 1
        assert total == 10
        assert outcome == 'possible botch'

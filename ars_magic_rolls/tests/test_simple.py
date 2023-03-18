# Tests for simple die rolls


from mock import Mock, patch

from ..simple import simple_roll


def test_simple_roll_normal():
    """Test that we get the expected result for a non-one, non-zero roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        rolls, total, outcome = simple_roll(10)
        assert len(rolls) == 1
        assert total == 16
        assert outcome == ''


def test_simple_roll_one():
    """Test that a one is treated as a one"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 6]):
        rolls, total, outcome = simple_roll(10)
        assert len(rolls) == 1
        assert total == 11
        assert outcome == ''


def test_simple_roll_zero():
    """Test that 0's are treated as just zero"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        rolls, total, outcome = simple_roll(10)
        assert len(rolls) == 1
        assert total == 10
        assert outcome == ''


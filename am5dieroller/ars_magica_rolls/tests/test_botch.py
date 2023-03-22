"""Test for botch rolls"""

from unittest.mock import Mock, patch

from ..botch import botch_roll


def test_no_botch_single():
    """Test that we can get no botches on a single roll"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        rolls, botches, outcome = botch_roll(1)
        assert len(rolls) == 1
        assert botches == 0
        assert outcome == 'no botch'


def test_no_botch_three():
    """Test that we can get no botches on a three dice"""
    with patch('random.randint', new_callable=Mock, side_effect=[6, 7, 1, 2, 3]):
        rolls, botches, outcome = botch_roll(3)
        assert len(rolls) == 3
        assert botches == 0
        assert outcome == 'no botch'


def test_no_botch_ten():
    """Test that we can get no botches on ten dice"""
    with patch('random.randint', new_callable=Mock, side_effect=[6, 7, 1, 2, 3, 1, 2, 3, 4, 5]):
        rolls, botches, outcome = botch_roll(10)
        assert len(rolls) == 10
        assert botches == 0
        assert outcome == 'no botch'


def test_single_botch_single():
    """Test that we can see a single botch on a single die"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        rolls, botches, outcome = botch_roll(1)
        assert len(rolls) == 1
        assert botches == 1
        assert outcome == 'botched'



def test_single_botch_five():
    """Test that we can see a single botch on five die"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 2, 0, 3, 4]):
        rolls, botches, outcome = botch_roll(5)
        assert len(rolls) == 5
        assert botches == 1
        assert outcome == 'botched'


def test_three_botch_three():
    """Test that we can see three botches on three die"""
    with patch('random.randint', new_callable=Mock, side_effect=[0, 0, 0]):
        rolls, botches, outcome = botch_roll(3)
        assert len(rolls) == 3
        assert botches == 3
        assert outcome == 'botched'


def test_three_botch_ten():
    """Test that we can see three botches on ten die"""
    with patch('random.randint', new_callable=Mock,
               side_effect=[7, 3, 0, 5, 7, 1, 0, 0, 4, 9, 1, 1, 3]):
        rolls, botches, outcome = botch_roll(10)
        assert len(rolls) == 10
        assert botches == 3
        assert outcome == 'botched'

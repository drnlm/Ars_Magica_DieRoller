# Test for spontaneous spell rolls

from mock import Mock, patch

from ..spont_rolls import spont_roll, fatiguing_spont_roll


def test_spont_success():
    """Test that a non-fatiguing spont can succeed"""
    # Should get 30 / 5 >= 5
    roll, total, result, outcome = spont_roll(30, 5)
    assert total == 30
    assert result == 6
    assert outcome == "success"


def test_spont_exact_success():
    """Test that a non-fatiguing spont can succeed at exactly the right number"""
    # Should get 25 / 5 == 5
    roll, total, result, outcome = spont_roll(25, 5)
    assert total == 25
    assert result == 5
    assert outcome == "success"


def test_spont_fail():
    """Test that a non-fatiguing spont can fail"""
    # Should get 30 / 5 < 10
    roll, total, result, outcome = spont_roll(30, 10)
    assert total == 30
    assert result == 6
    assert outcome == "failure"


def test_spont_neg_1_failure():
    """Test that a non-fatiguing spont fails if we're just short"""
    # It's not completely clear if we should round up here, as
    # it's one of the few places rounding isn't specified. We
    # assume no rounding, so misses by -1 fail
    # Should get 24 / 5 < 5
    roll, total, result, outcome = spont_roll(24, 5)
    assert total == 24
    assert result == 4
    assert outcome == "failure"


def test_fatiguing_spont_success():
    """Test that a fatiguing spont can succeed"""
    with patch('random.randint', new_callable=Mock, side_effect=[6]):
        # should get 31 / 2 > 5
        roll, total, result, outcome = fatiguing_spont_roll(25, 5)
        assert total == 31
        assert result == 15
        assert outcome == 'success'


def test_fatiguing_spont_fail():
    """Test that a fatiguing spont can fail"""
    with patch('random.randint', new_callable=Mock, side_effect=[2]):
        # should get 27 / 2 < 15
        roll, total, result, outcome = fatiguing_spont_roll(25, 15)
        assert total == 27
        assert result == 13
        assert outcome == 'failure'


def test_fatiguing_spont_possible_botch_or_success():
    """Test that a fatiguing spont can detect a possible botch which would succeed if 0"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        # should get 25 / 2 > 5
        roll, total, result, outcome = fatiguing_spont_roll(25, 5)
        assert total == 25
        assert result == 12
        assert 'possible success' in outcome
        assert 'possible botch' in outcome


def test_fatiguing_spont_possible_botch_or_failure():
    """Test that a fatiguing spont can detect a possible botch"""
    with patch('random.randint', new_callable=Mock, side_effect=[0]):
        # should get 25 / 2 < 15
        roll, total, result, outcome = fatiguing_spont_roll(25, 15)
        assert total == 25
        assert result == 12
        assert 'failure' in outcome
        assert 'possible botch' in outcome


def test_fatiguing_spont_openend():
    """Test that a fatiguing spont can open-end"""
    with patch('random.randint', new_callable=Mock, side_effect=[1, 1, 6]):
        # should get 49 / 2 > 15
        roll, total, result, outcome = fatiguing_spont_roll(25, 15)
        assert total == 49
        assert result == 24
        assert 'success' in outcome


def test_fatiguing_spont_exact_success():
    """Test that a fatiguing spont can succeed at the exact margin"""
    with patch('random.randint', new_callable=Mock, side_effect=[5]):
        # should get 31 / 2 > 5
        roll, total, result, outcome = fatiguing_spont_roll(25, 15)
        assert total == 30
        assert result == 15
        assert outcome == 'success'


def test_fatiguing_spont_fail_neg_1():
    """Test that a fatiguing spont can fail if we just miss"""
    # See spont discussion about rounding
    with patch('random.randint', new_callable=Mock, side_effect=[2]):
        # should get 29/2 < 15
        roll, total, result, outcome = fatiguing_spont_roll(27, 15)
        assert total == 29
        assert result == 14
        assert outcome == 'failure'

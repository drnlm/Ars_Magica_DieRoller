from ..utils import die_roller


def test_die_roller():
    """Test that the die roller helper behaves as desired"""
    # Testing randomness is hard, so we don't do that
    # Instead we just test that we get the correct range
    # of values and get all the possible results
    # 1000 trails is comlete overkill here, but is
    # a number I like
    results = set()
    for trial in range(1000):
        results.add(die_roller())

    assert len(results) == 10
    assert 0 in results
    assert 1 in results
    assert 2 in results
    assert 3 in results
    assert 4 in results
    assert 5 in results
    assert 6 in results
    assert 7 in results
    assert 8 in results
    assert 9 in results

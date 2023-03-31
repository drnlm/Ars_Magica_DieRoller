# This tests the internal functions to make sure we're basically calling the right thing
# We don't try to mock out the actual discord API, relying on the discord.py people
# to handle that testing

from unittest.mock import Mock, patch

from ..internal import (stressed_internal, simple_internal, botch_internal,
                        formulaic_internal, formulaic_simple_internal,
                        spontaneous_internal, fspont_internal, ritual_internal)


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

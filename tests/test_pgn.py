import pgn
import pytest
import subprocess

@pytest.fixture
def compile_peg():
    print(subprocess.check_output(["canopy", "pgn.peg", "--lang", "python"]))

@pytest.mark.usefixtures("compile_peg")
class TestParseTagPairs(object):
    def test_parse_tag_pair(self):
        tag_pair = '[Site "chess.com"]'
        parsed = pgn.parse(tag_pair).elements[0]
        assert parsed.text is tag_pair
        assert parsed.key.text == "Site"
        assert parsed.value.text == "chess.com"

    def test_parse_tag_pair_newline(self):
        tag_pair = '[Site "chess.com"]\n'
        parsed = pgn.parse(tag_pair).elements[0]
        assert parsed.text is tag_pair
        assert parsed.key.text == "Site"
        assert parsed.value.text == "chess.com"

    def test_parse_tag_pairs(self):
        tag_pairs = '[Event "Let\'s Play!"]\n[Site "Chess.com"]'
        parsed = pgn.parse(tag_pairs)
        first = parsed.elements[0]
        assert first.text == '[Event "Let\'s Play!"]\n'
        assert first.key.text == "Event"
        assert first.value.text == "Let's Play!"
        second = parsed.elements[1]
        assert second.text == '[Site "Chess.com"]'
        assert second.key.text == "Site"
        assert second.value.text == "Chess.com"

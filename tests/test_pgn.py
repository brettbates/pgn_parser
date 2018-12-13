import pgn
from pgn_parser import Actions
import pytest
import subprocess

@pytest.fixture
def compile_peg():
    print(subprocess.call(["canopy", "pgn.peg", "--lang", "python"]))

@pytest.mark.usefixtures("compile_peg")
class TestParseTagPairs(object):
    def test_parse_tag_pair(self):
        tag_pair = '[Site "chess.com"]'
        tag_pairs = pgn.parse(tag_pair, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"

    def test_parse_tag_pair_newline(self):
        tag_pair = '[Site "chess.com"]\n'
        tag_pairs = pgn.parse(tag_pair, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"

    def test_parse_tag_pairs(self):
        tag_pairs = '[Event "Let\'s Play!"]\n[Site "chess.com"]'
        tag_pairs = pgn.parse(tag_pairs, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"
        assert tag_pairs['Event'] == "Let\'s Play!"

@pytest.mark.usefixtures("compile_peg")
class TestParseMovetext(object):
    def test_parse_movetext_simple(self):
        moves = '1. e4 e5'
        parsed = pgn.parse(moves, actions=Actions()).movetext.elements[0]
        assert parsed.text == moves
        assert parsed.move_number.text == "1."
        assert parsed.white.text == "e4"
        assert parsed.black.text == "e5"

    def test_parse_movetext_simple_BN(self):
        moves = '2. Bb5 Nc6'
        parsed = pgn.parse(moves, actions=Actions()).movetext.elements[0]
        assert parsed.text == moves
        assert parsed.move_number.text == "2."
        assert parsed.white.text == "Bb5"
        assert parsed.black.text == "Nc6"

    def test_parse_movetexts_simple_space(self):
        moves = '1. e4 e5 2. d4 d5'
        parsed = pgn.parse(moves, actions=Actions()).movetext
        first = parsed.elements[0]
        second = parsed.elements[1]
        assert first.move_number.text == "1."
        assert first.white.text == "e4"
        assert first.black.text == "e5"
        assert second.move_number.text == "2."
        assert second.white.text == "d4"
        assert second.black.text == "d5"

    def test_parse_movetexts_simple_newline(self):
        moves = '1. e4 e5\n2. d4 d5'
        parsed = pgn.parse(moves, actions=Actions()).movetext
        first = parsed.elements[0]
        second = parsed.elements[1]
        assert first.move_number.text == "1."
        assert first.white.text == "e4"
        assert first.black.text == "e5"
        assert second.move_number.text == "2."
        assert second.white.text == "d4"
        assert second.black.text == "d5"

    def test_parse_movetexts_simple_newline_mid(self):
        moves = '1. e4 e5 2. d4\nd5'
        parsed = pgn.parse(moves, actions=Actions()).movetext
        first = parsed.elements[0]
        second = parsed.elements[1]
        assert first.move_number.text == "1."
        assert first.white.text == "e4"
        assert first.black.text == "e5"
        assert second.move_number.text == "2."
        assert second.white.text == "d4"
        assert second.black.text == "d5"

    def test_parse_movetexts_comment(self):
        moves = '1. e4 e5 {comment 1...} 2. d4 {comment 2.} d5'
        parsed = pgn.parse(moves, actions=Actions()).movetext
        first = parsed.elements[0]
        second = parsed.elements[1]
        assert first.move_number.text == "1."
        assert first.white.text == "e4"
        assert first.black.text == "e5"
        assert first.bcomment == "comment 1..."
        assert second.move_number.text == "2."
        assert second.white.text == "d4"
        assert second.wcomment == "comment 2."
        assert second.black.text == "d5"

import pgn
from pgn_parser import Actions
import pytest
import subprocess

@pytest.fixture
def compile_peg():
    print(subprocess.call(["canopy", "pgn.peg", "--lang", "python"]))
    return

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

    def test_parse_tag_pairs_space(self):
        tag_pairs = '[Event "Let\'s Play!"] [Site "chess.com"]'
        tag_pairs = pgn.parse(tag_pairs, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"
        assert tag_pairs['Event'] == "Let\'s Play!"


@pytest.mark.usefixtures("compile_peg")
class TestParseMovetext(object):
    def test_parse_movetext_simple(self):
        moves = '1. e4 e5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == "e4"
        assert movetext.black.san == "e5"

    def test_parse_movetext_simple_BN(self):
        moves = '2. Bb5 Nc6'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 2
        assert movetext.white.san == "Bb5"
        assert movetext.black.san == "Nc6"

    def test_parse_movetexts_simple_space(self):
        moves = '1. e4 e5 2. d4 d5'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        first = movetext[0]
        second = movetext[1]
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].black.san == "d5"

    def test_parse_movetexts_simple_newline(self):
        moves = '1. e4 e5\n2. d4 d5'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        movetext[0] = movetext[0]
        movetext[1] = movetext[1]
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].black.san == "d5"

    def test_parse_movetexts_simple_newline_mid(self):
        moves = '1. e4 e5 2. d4\nd5'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        movetext[0] = movetext[0]
        movetext[1] = movetext[1]
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].black.san == "d5"

    def test_parse_movetexts_comment(self):
        moves = '1. e4 e5 {comment 1...} 2. d4 {comment 2.} d5'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        movetext[0] = movetext[0]
        movetext[1] = movetext[1]
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[0].black.comment == "comment 1..."
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].white.comment == "comment 2."
        assert movetext[1].black.san == "d5"

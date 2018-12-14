import pgn
from pgn_parser import Actions
import pytest
import subprocess

@pytest.fixture
def compile_peg():
    print(subprocess.call(["canopy", "pgn.peg", "--lang", "python"]))
    return

@pytest.mark.usefixtures("compile_peg")
@pytest.mark.tp
class TestParseTagPairs(object):
    def test_parse_tag_pair(self):
        tag_pair = '[Site "chess.com"]'
        tag_pairs = pgn.parse(tag_pair, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"

    def test_parse_tag_pair_1n(self):
        tag_pair = '[Site\n"chess.com"]'
        tag_pairs = pgn.parse(tag_pair, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"

    def test_parse_tag_pair_2n(self):
        tag_pair = '[Site\n"chess.com"\n]'
        tag_pairs = pgn.parse(tag_pair, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"

    def test_parse_tag_pair_3n(self):
        tag_pair = '[\nSite\n"chess.com"\n]'
        tag_pairs = pgn.parse(tag_pair, actions=Actions()).tag_pairs
        assert tag_pairs['Site'] == "chess.com"

    def test_parse_tag_pair_3ws(self):
        tag_pair = '[ Site\n"chess.com"\t]'
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
@pytest.mark.mt
class TestParseMovetext(object):
    def test_parse_movetext_simple(self):
        moves = '1. e4 e5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == "e4"
        assert movetext.black.san == "e5"

    def test_parse_san_piece_takes(self):
        moves = '1. Nxd5 Bxd5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == "Nxd5"
        assert movetext.black.san == "Bxd5"

    def test_parse_san_pawn_takes(self):
        moves = '1. exd5 cxd5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == "exd5"
        assert movetext.black.san == "cxd5"

    def test_parse_san_pawn_promotes(self):
        moves = '9. a8=Q axb8=R'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 9
        assert movetext.white.san == "a8=Q"
        assert movetext.black.san == "axb8=R"

    def test_parse_san_check(self):
        moves = '9. a8+ axb8=R#'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 9
        assert movetext.white.san == "a8+"
        assert movetext.black.san == "axb8=R#"

    def test_parse_san_castle(self):
        moves = '9. O-O O-O-O'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 9
        assert movetext.white.san == "O-O"
        assert movetext.black.san == "O-O-O"

    def test_parse_san_disambiguation_file(self):
        moves = '9. Ncxd5 Nce5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 9
        assert movetext.white.san == "Ncxd5"
        assert movetext.black.san == "Nce5"

    def test_parse_san_disambiguation_rank(self):
        moves = '9. N3xd5 N6e5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 9
        assert movetext.white.san == "N3xd5"
        assert movetext.black.san == "N6e5"

    def test_parse_san_disambiguation_square(self):
        moves = '9. Nc3xd5 Nc6e5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 9
        assert movetext.white.san == "Nc3xd5"
        assert movetext.black.san == "Nc6e5"

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

@pytest.mark.usefixtures("compile_peg")
class TestParse:
    @pytest.mark.score
    def test_parse_score(self):
        moves = "[Site \"help\"]\n1. e4 e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "1-0"

@pytest.mark.usefixtures("compile_peg")
class TestGame:
    @pytest.mark.score
    def test_parse_game(self):
        moves = "[Site \"help\"]\n1. e4 e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.tag_pairs['Site'] == "help"
        assert parsed.movetext[0].white.san == "e4"
        assert parsed.movetext[0].black.san == "e5"
        assert parsed.score.result == "1-0"

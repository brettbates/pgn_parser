import pgn
from pgn_parser import Actions
import pytest
import subprocess


@pytest.mark.tp
class TestParseTagPairs(object):
    """Test the parsing of tag pairs

    Each test is a tag_pair(s) that should be parsed and accessible as a dictionary
    """

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


@pytest.mark.mt
class TestParseMovetext(object):
    """Test the parsing of movetext

    Each test is an input move or set of moves to be converted to an List of Move's
    """
    def test_parse_movetext_simple(self):
        moves = '1. e4 e5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == "e4"
        assert movetext.black.san == "e5"

    def test_parse_movetext_single_ply(self):
        moves = '1. e4'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == "e4"
        assert movetext.black.san == ""

    def test_parse_movetext_single_ply_black(self):
        moves = '1...e5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == ""
        assert movetext.black.san == "e5"

    def test_parse_movetext_single_ply_blacksp(self):
        moves = '1... e5'
        movetext = pgn.parse(moves, actions=Actions()).movetext[0]
        assert movetext.move_number == 1
        assert movetext.white.san == ""
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
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].black.san == "d5"

    def test_parse_movetexts_simple_newline(self):
        moves = '1. e4 e5\n2. d4 d5'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].black.san == "d5"

    def test_parse_movetexts_simple_newline_mid(self):
        moves = '1. e4 e5 2. d4\nd5'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].black.san == "d5"

    def test_parse_movetexts_comment(self):
        moves = '1. e4 e5 {comment 1...} 2. d4 {comment 2.} d5'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].black.san == "e5"
        assert movetext[0].black.comment == "comment 1..."
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].white.comment == "comment 2."
        assert movetext[1].black.san == "d5"

    def test_parse_movetexts_nag_single(self):
        moves = '1. e4 $0 e5 $139'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].white.nags == ["$0"]
        assert movetext[0].black.san == "e5"
        assert movetext[0].black.nags == ["$139"]

    def test_parse_movetexts_nag_multiple(self):
        moves = '1. e4 $0 $19 e5 $19 $139 $0'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].white.nags == ["$0", "$19"]
        assert movetext[0].black.san == "e5"
        assert movetext[0].black.nags == ["$19", "$139", "$0"]

    def test_parse_movetexts_nags(self):
        moves = '1. e4 $0 e5 $1 $139 {comment 1...} 2. d4 $3 {comment 2.} d5 $19 $21 $139 $0'
        movetext = pgn.parse(moves, actions=Actions()).movetext
        assert movetext[0].move_number == 1
        assert movetext[0].white.san == "e4"
        assert movetext[0].white.nags == ["$0"]
        assert movetext[0].black.san == "e5"
        assert movetext[0].black.nags == ["$1", "$139"]
        assert movetext[0].black.comment == "comment 1..."
        assert movetext[1].move_number == 2
        assert movetext[1].white.san == "d4"
        assert movetext[1].white.nags == ["$3"]
        assert movetext[1].white.comment == "comment 2."
        assert movetext[1].black.san == "d5"
        assert movetext[1].black.nags == ["$19", "$21", "$139", "$0"]

class TestGame:
    """Test the parsing of an entire game

    Given a full game, product a valid Game object representing the input
    """
    def test_parse_game(self):
        moves = "[Site \"help\"]\n1. e4 e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.tag_pairs['Site'] == "help"
        assert parsed.movetext[0].white.san == "e4"
        assert parsed.movetext[0].black.san == "e5"
        assert parsed.score.result == "1-0"

    def test_parse_game_variations(self):
        moves = "[Site \"help\"]\n1. e4 (1. d4 d5) e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.movetext[0].white.variations[0][0].white.san == "d4"
        assert parsed.movetext[0].white.variations[0][0].black.san == "d5"

    @pytest.mark.wip
    def test_parse_game_variations_2o(self):
        moves = "[Site \"help\"]\n1. e4 (1. d4 d5) (1. c4 e5) e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.movetext[0].white.variations[1][0].white.san == "c4"
        assert parsed.movetext[0].white.variations[1][0].black.san == "e5"

    @pytest.mark.wip
    def test_parse_game_variations_2o_multi(self):
        moves = "[Site \"help\"]\n1. e4 (1. d4 d5 2. c4 e6) (1. c4 c5 2. g3 e6) e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.movetext[0].white.variations[1][0].white.san == "c4"
        assert parsed.movetext[0].white.variations[1][0].black.san == "c5"
        assert parsed.movetext[0].white.variations[1][1].white.san == "g3"
        assert parsed.movetext[0].white.variations[1][1].black.san == "e6"

    @pytest.mark.wip
    def test_parse_game_variations_3o(self):
        moves = "[Site \"help\"]\n1. e4 (1. d4 d5) (1. c4 e5) (1. a4 h5) e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.movetext[0].white.variations[0][0].white.san == "d4"
        assert parsed.movetext[0].white.variations[0][0].black.san == "d5"
        assert parsed.movetext[0].white.variations[1][0].white.san == "c4"
        assert parsed.movetext[0].white.variations[1][0].black.san == "e5"
        assert parsed.movetext[0].white.variations[2][0].white.san == "a4"
        assert parsed.movetext[0].white.variations[2][0].black.san == "h5"

    def test_parse_game_variations_multi(self):
        moves = "[Site \"help\"]\n1. e4 (1. d4 d5 2. c4 c5) e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.movetext[0].white.variations[0][0].white.san == "d4"
        assert parsed.movetext[0].white.variations[0][1].black.san == "c5"

    def test_parse_game_variations_black(self):
        moves = "[Site \"help\"]\n1. e4 e5 (1...d5) 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.movetext[0].black.variations[0][0].black.san == "d5"

    def test_parse_game_variations_multi_black(self):
        moves = "[Site \"help\"]\n1. e4 e5 (1...d5 2. c4 c5) 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.movetext[0].black.variations[0][0].white.san == ""
        assert parsed.movetext[0].black.variations[0][0].black.san == "d5"
        assert parsed.movetext[0].black.variations[0][1].black.san == "c5"

    def test_parse_score(self):
        moves = "[Site \"help\"]\n1. e4 e5 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "1-0"

    def test_parse_score_single_ply_white(self):
        moves = "[Site \"help\"]\n1. e4 1-0"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "1-0"

    def test_parse_score_single_ply_black(self):
        moves = "[Site \"help\"]\n1...e5 0-1"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "0-1"

    def test_parse_score_single_ply_unknown_white(self):
        moves = "[Site \"tst\"]\n1. e4 *"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "*"

    def test_parse_score_no_tp_single_ply_unknown_white(self):
        moves = "11. Kxc4 *"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "*"

    def test_parse_score_single_ply_unknown_black(self):
        moves = "[Site \"tst\"]\n1...e4 *"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "*"

    def test_parse_newline_sore(self):
        moves = "[Site \"tst\"]\n1. Kxh2\nQxf4+ 0-1"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "0-1"

    def test_parse_arbitrary_space(self):
        moves = "[Site \"tst\"]\n1. Kxh2\nQxf4+ 0-1 "
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "0-1"

    def test_parse_arbitrary_space_n(self):
        moves = "[Site \"tst\"]\n1. Kxh2\nQxf4+ 0-1\n"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "0-1"

    def test_parse_arbitrary_space_sn(self):
        moves = "[Site \"tst\"]\n1. Kxh2\nQxf4+ 0-1 \n"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "0-1"

    def test_parse_arbitrary_space_any(self):
        moves = "[Site \"tst\"]\n1. Kxh2\nQxf4+ 0-1\n \n\t    \n"
        parsed = pgn.parse(moves, actions=Actions())
        assert parsed.score.result == "0-1"

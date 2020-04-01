import pgn_parser.parser as parser
from pgn_parser.pgn import Actions, Move, Score, Ply, PGNGameException
import pytest
from unittest.mock import MagicMock


def make_move_node(text, move_number, white, wcomment, black, bcomment, mcomment):
    """Create a mock set of nodes that comprise a Game"""
    n = MagicMock(
        move_number = parser.TreeNode(move_number, 0),
        white = parser.TreeNode(white, 0),
        wcomment = wcomment,
        black = parser.TreeNode(black, 0),
        bcomment = bcomment,
        mcomment = mcomment)
    return n

def make_nags_move_node(text, move_number, white, wnags, wcomment, black, bnags, bcomment):
    """Create a mock set of nodes that comprise a Game"""
    wnagsn = parser.TreeNode(wnags, 0)
    bnagsn = parser.TreeNode(bnags, 0)
    wnagsn.elements = [parser.TreeNode(n, 0) for n in wnags.split(' ')]
    bnagsn.elements = [parser.TreeNode(n, 0) for n in bnags.split(' ')]
    n = MagicMock(
        move_number = parser.TreeNode(move_number, 0),
        white = parser.TreeNode(white, 0),
        wnags = wnagsn,
        wcomment = wcomment,
        black = parser.TreeNode(black, 0),
        bnags = bnagsn,
        bcomment = bcomment)
    return n

def make_nodes(eles):
    """Create a list of TreeNode's for feeding to the make_ actions"""
    out = []
    for e in eles:
        out.append(parser.TreeNode(e, 0))
    return out

class TestParserActions:
    """Testing the Actions class as an actions object for use by the parser"""

    def test_make_tag_pair(self):
        tp = Actions().make_tag_pair('[Event "test"]', 0, 0, make_nodes(["[", "", "Event", "", " \"", "test", "\"", "", "]"]))
        assert tp['Event'] == "test"

    def test_make_tag_pairs(self):
        tp = Actions().make_tag_pairs('[Event "test"]\n[Site "bmb.io"]', 0, 0, [{'Event': 'test'}, {'Site': 'bmb.io'}])
        assert tp['Event'] == "test"
        assert tp['Site'] == "bmb.io"

    def test_make_movetext_simple(self):
        mtt = '1. e4 e5'
        mt = Actions().make_movetext(mtt, 0, 0,
                                     [make_move_node(mtt, "1.", "e4", "", "e5", "", "")])
        assert mt[0].move_number == 1
        assert mt[0].white.san == "e4"
        assert mt[0].black.san == "e5"

    def test_make_movetext_comment(self):
        mtt = '1. e4 {white comment} e5 {black comment} {move comment}'
        mt = Actions().make_movetext(mtt, 0, 0,
                                     [make_move_node(mtt, "1.", "e4", "white comment", "e5", "black comment", "move comment")])
        assert mt[0].move_number == 1
        assert mt[0].white.san == "e4"
        assert mt[0].white.comment == "white comment"
        assert mt[0].black.san == "e5"
        assert mt[0].black.comment == "black comment"
        assert mt[0].comment == "move comment"

    def test_make_movetext_nags(self):
        mtt = '1. e4 $1 e5 $19 $139'
        mt = Actions().make_movetext(mtt, 0, 0,
                                     [make_nags_move_node(mtt, "1.", "e4", "$1", "", "e5", "$19 $139", "")])
        assert mt[0].move_number == 1
        assert mt[0].white.san == "e4"
        assert mt[0].white.nags == ["$1"]
        assert mt[0].black.san == "e5"
        assert mt[0].black.nags == ["$19", "$139"]

    def test_make_game(self):
        input = '[Site "bmb.io]\n1. e4 e5 {white wins} 1-0'
        g = Actions().make_game(input, 0, 0,
                                     [{'Site': 'bmb.io'},
                                      parser.TreeNode('\n', 0),
                                      "",
                                      [Move("1.", "e4", "", "", [], "e5", "", "white wins", [], "")],
                                      parser.TreeNode('1-0', 0)])
        assert g.tag_pairs['Site'] == "bmb.io"
        assert g.movetext[0].move_number == 1
        assert g.movetext[0].white.san == "e4"
        assert g.movetext[0].black.san == "e5"
        assert g.movetext[0].black.comment == "white wins"
        assert g.score.result == "1-0"

    def test_make_game_variations(self):
        input = '[Site "bmb.io]\n1. e4 (1. d4) e5 {white wins} 1-0'
        g = Actions().make_game(input, 0, 0,
                                     [{'Site': 'bmb.io'},
                                      parser.TreeNode('\n', 0),
                                      "",
                                      [Move("1.", "e4", "", "",
                                            [[Move("1.", "d4", "", "", "", "", "", "", "", "")]],
                                            "e5", "", "white wins", [], "")],
                                      parser.TreeNode('1-0', 0)])
        assert g.tag_pairs['Site'] == "bmb.io"
        assert g.movetext[0].white.variations[0][0].move_number == 1
        assert g.movetext[0].white.variations[0][0].white.san == "d4"

    def test_make_game_gcomment(self):
        input = '[Site "bmb.io"]\n{game comment} 1. e4 e5 {white wins} 1-0'
        g = Actions().make_game(input, 0, 0,
                                     [{'Site': 'bmb.io'},
                                      parser.TreeNode('\n', 0),
                                      "game comment",
                                      [Move("1.", "e4", "", "", [], "e5", "", "white wins", [], "")],
                                      parser.TreeNode('1-0', 0)])
        assert g.tag_pairs['Site'] == "bmb.io"
        assert g.comment == "game comment"
        assert g.movetext[0].move_number == 1
        assert g.movetext[0].white.san == "e4"
        assert g.movetext[0].black.san == "e5"
        assert g.movetext[0].black.comment == "white wins"
        assert g.score.result == "1-0"


class TestGame:
    """Testing Game Objects"""
    def test_get_move(self):
        """Given a move number retrieve that move"""
        input = '[Site "bmb.io"]\n{game comment} 35. e4 e5 36. d4 d5 37. c4 c5 {white wins} 1-0'
        g = parser.parse(input, actions=Actions())
        assert str(g.move(35)) == "35. e4 e5"

    def test_get_move_0(self):
        """Given a move number retrieve that move"""
        input = '[Site "bmb.io"]\n{game comment} 35. e4 e5 36. d4 d5 37. c4 c5 {white wins} 1-0'
        g = parser.parse(input, actions=Actions())
        with pytest.raises(PGNGameException):
            g.move(0)

    def test_get_move_too_low(self):
        """Given a move number retrieve that move"""
        input = '[Site "bmb.io"]\n{game comment} 35. e4 e5 36. d4 d5 37. c4 c5 {white wins} 1-0'
        g = parser.parse(input, actions=Actions())
        with pytest.raises(PGNGameException):
            g.move(34)

    def test_get_move_too_high(self):
        """Given a move number retrieve that move"""
        input = '[Site "bmb.io"]\n{game comment} 35. e4 e5 36. d4 d5 37. c4 c5 {white wins} 1-0'
        g = parser.parse(input, actions=Actions())
        with pytest.raises(PGNGameException):
            g.move(39)


class TestTagPairs:
    """Testing TagPair objects"""

    def test_str_ordered(self):
        """Given a set of tag pairs, ensure an ordered STR"""
        input =  '[Date "now"]\n[Site "bmb.io"]\n[Event "here"]\n{game comment} 1. e4 e5 {white wins} 1-0'
        expect = '[Event "here"]\n[Site "bmb.io"]\n[Date "now"]\n\n{game comment} 1. e4 e5 {white wins} 1-0'
        assert str(parser.parse(input, actions=Actions())) == expect

    def test_str_extra(self):
        """Given a set of tag pairs, ensure an ordered STR"""
        input =  '[Extra "tp"]\n[Date "now"]\n[Site "bmb.io"]\n[Event "here"]\n{game comment} 1. e4 e5 {white wins} 1-0'
        expect = '[Event "here"]\n[Site "bmb.io"]\n[Date "now"]\n[Extra "tp"]\n\n{game comment} 1. e4 e5 {white wins} 1-0'
        actual = str(parser.parse(input, actions=Actions()))
        assert actual == expect

class TestMove:
    """Testing Move objects"""

    def test_move_no_to_i(self):
        """Test converting a string move number like 1. into the int 1"""
        f = Move("1.","","","","","","","","", "").move_no_to_i
        assert f("1.") == 1
        assert f("2.") == 2
        assert f("300.") == 300


class TestPly:
    """Testing Ply objects"""

    def test_nodes_to_nags(self):
        p = Ply("1.", "e4", nags=make_nodes(["$1", "$19", "$139"]))
        assert p.nags == ["$1", "$19", "$139"]


class TestScore:
    """Testing the construction of a Score object"""

    def test_make_score(self):
        assert Score("0-1").white == "0"
        assert Score("0-1").black == "1"
        assert Score("0-1").result == "0-1"
        assert Score("1-0").white == "1"
        assert Score("1-0").black == "0"
        assert Score("1-0").result == "1-0"
        assert Score("1/2-1/2").white == "1/2"
        assert Score("1/2-1/2").black == "1/2"
        assert Score("1/2-1/2").result == "1/2-1/2"
        assert Score("*").result == "*"

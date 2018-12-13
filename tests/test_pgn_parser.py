import pgn
from pgn_parser import Actions
import pytest


def make_nodes(eles):
    out = []
    for e in eles:
        out += pgn.TreeNode(e, 0)
    return out

class TestParserActions(object):
    def test_make_tag_pair(self):
        tp = Actions().make_tag_pair('[Event "test"]', 0, 0, make_nodes("[", "Event", " \"", "test", "]"))
        assert tp['Event'] == "test"

    def test_make_tag_pairs(self):
        tp = Actions().make_tag_pairs('[Event "test"]\n[Site "bmb.io"]', 0, 0, [{'Event': 'test'}, {'Site': 'bmb.io'}])
        assert tp['Event'] == "test"
        assert tp['Site'] == "bmb.io"

    def test_make_movetext_simple(self):
        mt = Actions().make_movetext('1. e4 e5', 0, 0, make_nodes(["1.", " ", "e4", " ", "e5"]))
        assert mt[0].move_number == 1
        assert mt[0].white.san == "e4"
        assert mt[0].black.san == "e5"

    def test_make_movetext_comment(self):
        mt = Actions().make_movetext('1. e4 {white comment} e5 {black comment}', 0, 0,
                                     make_nodes(["1.", " ", "e4", " ", "e5"]))
        assert mt[0].move_number == 1
        assert mt[0].white.san == "e4"
        assert mt[0].white.comment == "white comment"
        assert mt[0].black.san == "e5"
        assert mt[0].black.comment == "black comment"


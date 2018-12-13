import pgn
from pgn_parser import Actions
import pytest

class TestParserActions(object):
    def test_make_tag_pair(self):
        tp = Actions().make_tag_pair('[Event "test"]', 0, 14, [pgn.TreeNode("[", 0),
                                                               pgn.TreeNode("Event", 0),
                                                               pgn.TreeNode(" \"", 0),
                                                               pgn.TreeNode("test", 0),
                                                               pgn.TreeNode("]", 0)])
        assert tp['Event'] == "test"

    def test_make_tag_pairs(self):
        tp = Actions().make_tag_pairs('[Event "test"]\n[Site "bmb.io"]', 0, 14, [{'Event': 'test'}, {'Site': 'bmb.io'}])
        assert tp['Event'] == "test"
        assert tp['Site'] == "bmb.io"


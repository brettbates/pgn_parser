import pgn
import difflib
import os
from pgn_parser import Actions
from behave import given, when, then
from hamcrest import assert_that, has_item, equal_to


@given(u'a pgn file with only a header of the tag pairs {tag_pairs}')
def step_a_pgn_file_with_tag_pair(context, tag_pairs):
    context.pgn_str = tag_pairs.replace("\\n", "\n")


@when(u'we parse it')
def step_we_parse_it(context):
    context.pgn = pgn.parse(context.pgn_str, actions=Actions())


@then(u'we can access a TagPair of k {tag_key}, v {tag_value}')
def step_we_can_access_a_TagPair(context, tag_key, tag_value):
    assert_that(context.pgn.tag_pairs, has_item(tag_key))
    assert_that(context.pgn.tag_pairs[tag_key], equal_to(tag_value))


@then(u'we can access a fully populated TagPairs dict {tp_res}')
def step_we_can_access_tagpairs(context, tp_res):
    TEST_TP_RES = {
        "TEST_TP_2_RES": {"Event": "Let's Play!", "Site": "Chess.com"},
        "TEST_TP_3_RES": {"Event": "Let's Play!", "Site": "Chess.com", "Date": "2018.12.13"}}
    r = TEST_TP_RES[tp_res]
    for k in r.keys():
        assert_that(context.pgn.tag_pairs, has_item(k))
        assert_that(context.pgn.tag_pairs[k], equal_to(r[k]))

@given(u'a pgn file with only movetext {movetext}')
def step_a_movetext_only_pgn(context, movetext):
    context.pgn_str = movetext.replace("\\n", "\n")


@then(u'we can access the moves node containing an array of correct Move objects with SAN\'s {sanw} {sanb}')
def step_we_can_access_moves(context, sanw, sanb):
    for i, san in enumerate(sanw.split(',')):
        assert_that(context.pgn.movetext[i].white.san, equal_to(san))
        assert_that(context.pgn.movetext[i].black.san, equal_to(sanb.split(',')[i]))

@given(u'the pgn file {f}')
def step_a_pgn_file(context, f):
    path = "{}/features/steps/{}".format(os.getcwd(),f)
    context.pgn_str = open(path).read()


@then(u'we should have a full Game that can be stringified to equal the file {g}')
def step_test_full_game_file(context, g):

    correct = open('./features/steps/'+g).read()
    diff = difflib.ndiff(correct.splitlines(1), str(context.pgn).splitlines(1))
    for l in diff:
        print(l)
    assert_that(len(list(diff)), equal_to(0))

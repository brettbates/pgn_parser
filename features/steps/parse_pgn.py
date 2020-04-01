import pgn_parser.parser as parser
import difflib
import os
from pgn_parser.pgn import Actions
from behave import given, when, then
from hamcrest import assert_that, has_item, equal_to


@given(u'a pgn file with only a header of the tag pairs {tag_pairs}')
def step_a_pgn_file_with_tag_pair(context, tag_pairs):
    context.pgn_str = tag_pairs.replace("\\n", "\n")


@when(u'we parse it')
def step_we_parse_it(context):
    context.pgn = parser.parse(context.pgn_str, actions=Actions())


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

@then(u'we can string a TagPairs dict in order {tp_res}')
def step_string_tagpairs_ordered(context, tp_res):
    TEST_TP_RES = {
            "TEST_TP_3_RES_ORD": '[Event "Let\'s Play!"]\n[Site "Chess.com"]\n[Date "2018.12.13"]\n\n',
            "TEST_TP_4_RES_ORD": '[Event "Let\'s Play!"]\n[Site "Chess.com"]\n[Custom "xyz"]\n\n',
            "TEST_TP_5_RES_ORD": '[Event "Let\'s Play!"]\n[Site "Chess.com"]\n[Custom "xyz"]\n[Custom2 "xyz2"]\n[Custom3 "xyz3"]\n\n'}
    r = TEST_TP_RES[tp_res]
    assert_that(str(context.pgn.tag_pairs), equal_to(r))


@given(u'a pgn file with only movetext {movetext}')
def step_a_movetext_only_pgn(context, movetext):
    context.pgn_str = movetext.replace("\\n", "\n")


@then(u'we can access the moves node containing an array of correct Move objects with SAN\'s {sanw} {sanb}')
def step_we_can_access_moves(context, sanw, sanb):
    for i, san in enumerate(sanw.split(',')):
        sw = san if san != "NONE" else ""
        sb = sanb.split(',')[i] if sanb.split(',')[i] != "NONE" else ""
        assert_that(context.pgn.movetext[i].white.san, equal_to(sw))
        assert_that(context.pgn.movetext[i].black.san, equal_to(sb))

@given(u'the pgn file {f}')
def step_a_pgn_file(context, f):
    path = "{}/features/steps/test_data/{}".format(os.getcwd(),f)
    context.pgn_str = open(path).read()


@then(u'we should have a full Game that can be stringified to equal its input {g}')
def step_test_full_game_file(context, g):
    correct = open('./features/steps/test_data/'+g).read()
    diff = difflib.ndiff(correct.splitlines(1), str(context.pgn).splitlines(1))
    ds = list(diff)
    print("*" * 80)
    print("Parsed:")
    print("*" * 80)
    print(context.pgn)
    print('')
    print("*" * 80)
    print("Expected:")
    print("*" * 80)
    print(correct)
    print('')
    print("*" * 80)
    print("Diffs:")
    print("*" * 80)
    [print(d, end='') for d in ds]
    assert_that(str(context.pgn), equal_to(correct))

@then(u'we can access the comment and moves {sanw} {commw} {sanb} {commb} {commm}')
def step_we_can_access_comments(context, sanw, commw, sanb, commb, commm):
    if commw == "NONE":
        commw = ""
    elif commw == "SPACE":
        commw = " "
    elif commw == "\\n":
        commw = "\n"
    elif commw == "CLK":
        commw = " [%clk 0:03:00] "

    if commb == "NONE":
        commb = ""
    elif commb == "SPACE":
        commb = " "
    elif commb == "\\n":
        commb = "\n"
    elif commb == "CLK":
        commb = " [%clk 0:03:00] "

    if commm == "NONE":
        commm = ""
    elif commm == "SPACE":
        commm = " "
    elif commm == "\\n":
        commm = "\n"


    for i, san in enumerate(sanw.split(',')):
        assert_that(context.pgn.movetext[i].white.san, equal_to(san))
        assert_that(context.pgn.movetext[i].white.comment, equal_to(commw))
        assert_that(context.pgn.movetext[i].black.san, equal_to(sanb.split(',')[i]))
        assert_that(context.pgn.movetext[i].black.comment, equal_to(commb))
        assert_that(context.pgn.movetext[i].comment.strip(), equal_to(commm))

@then(u'we can access the variations 1. d4')
def step_var_1d4(context):
     assert_that(str(context.pgn.movetext[0].white.variations[0][0].white.san), equal_to("d4"))


@then(u'we can access the variations 1...d5')
def step_var_1bd5(context):
     assert_that(str(context.pgn.movetext[0].black.variations[0][0].black.san), equal_to("d5"))

@then(u'we can access the variations 1. d4 d5 2. c4 Nf6')
def step_var_2c4(context):
     assert_that(str(context.pgn.movetext[0].white.variations[0][1].white.san), equal_to("c4"))
     assert_that(str(context.pgn.movetext[0].white.variations[0][1].black.san), equal_to("Nf6"))

@then(u'we can access the variations 1. d4 d5,1. c4 e5')
def step_var_11d4d5(context):
     assert_that(str(context.pgn.movetext[0].white.variations[0][0].white.san), equal_to("d4"))
     assert_that(str(context.pgn.movetext[0].white.variations[0][0].black.san), equal_to("d5"))
     assert_that(str(context.pgn.movetext[0].white.variations[1][0].white.san), equal_to("c4"))
     assert_that(str(context.pgn.movetext[0].white.variations[1][0].black.san), equal_to("e5"))



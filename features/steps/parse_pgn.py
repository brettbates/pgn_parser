import pgn
from pgn_parser import Actions
from behave import given, when, then
from hamcrest import assert_that, has_item, equal_to


@given(u'a pgn file with only a header of the tag pair {tag_pair}')
def step_a_pgn_file_with_tag_pair(context, tag_pair):
    context.pgn_str = tag_pair


@when(u'we parse it')
def step_we_parse_it(context):
    context.pgn = pgn.parse(context.pgn_str, actions=Actions())


@then(u'we can access a TagPair of k {tag_key}, v {tag_value}')
def step_we_can_access_a_TagPair(context, tag_key, tag_value):
    assert_that(context.pgn.tag_pairs, has_item(tag_key))
    assert_that(context.pgn.tag_pairs[tag_key], equal_to(tag_value))

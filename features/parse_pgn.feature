Feature: Parsing a pgn file

    Scenario Outline: Parse a single tag_pair pgn header
        Given a pgn file with only a header of the tag pairs <tag_pairs>
         When we parse it
         Then we can access a TagPair of k <tp_k>, v <tp_v>

        Examples: Tag Pairs
            | tag_pairs               | tp_k  | tp_v        |
            | [Event "Let's Play!"]   | Event | Let's Play! |
            | [Site "Chess.com"]      | Site  | Chess.com   |

    Scenario Outline: Parse a multi tag_pair pgn header
        Given a pgn file with only a header of the tag pairs <tag_pairs>
         When we parse it
         Then we can access a fully populated TagPairs dict <tp_res>

        Examples: Tag Pairs
            | tag_pairs                                                     | tp_res        |
            | [Event "Let's Play!"]\n[Site "Chess.com"]                     | TEST_TP_2_RES |
            | [Event "Let's Play!"]\n[Site "Chess.com"] [Date "2018.12.13"] | TEST_TP_3_RES |

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


    Scenario Outline: Parse a pgn containing only movetext
        Given a pgn file with only movetext <movetext>
         When we parse it
         Then we can access the moves node containing an array of correct Move objects with SAN's <SANW> <SANB>

        Examples: Movetext
            | movetext            | SANW  | SANB   |
            | 1. e4 e5            | e4    | e5     |
            | 1. e4 e5\n2. d4 d5  | e4,d4 | e5,d5  | 
            | 1. e4 e5\n 2. d4 d5 | e4,d4 | e5,d5  |
            | 1. e4 e5 2.\nd4 d5  | e4,d4 | e5,d5  |
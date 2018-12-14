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
            | [Event "Let's Play!"] [Site "Chess.com"]                      | TEST_TP_2_RES |
            | [Event "Let's Play!"][Site "Chess.com"]                       | TEST_TP_2_RES |
            | [Event "Let's Play!"]\n[Site "Chess.com"] [Date "2018.12.13"] | TEST_TP_3_RES |


    @wip
    Scenario Outline: Parse a pgn containing only movetext
        Given a pgn file with only movetext <movetext>
         When we parse it
         Then we can access the moves node containing an array of correct Move objects with SAN's <SANW> <SANB>

        Examples: Movetext
            | movetext             | SANW   | SANB    |
            | 1. e4 e5             | e4     | e5      |
            | 1. e4 e5\n2. d4 d5   | e4,d4  | e5,d5   | 
            | 1. e4 e5\n2. Nf3 Nc6 | e4,Nf3 | e5,Nc6  | 
            | 1. e4 e5\n 2. d4 d5  | e4,d4  | e5,d5   |
            | 1. e4 e5 2.\nd4 d5   | e4,d4  | e5,d5   |
            | 12. Nxd5 Bxd5        | Nxd5   | Bxd5    |
            | 12. exd5 cxd5        | exd5   | cxd5    |
            | 9. a8=Q axb8=R       | a8=Q   | axb8=R  |
            | 9. a8+ axb8=R#       | a8+    | axb8=R# |
            | 9. O-O O-O-O         | O-O    | O-O-O   |
            | 9. Ncxd5 Nce5        | Ncxd5  | Nce5    |
            | 9. N3xd5 N6e5        | N3xd5  | N6e5    |
            | 9. Nc3xd5 Nc6e5      | Nc3xd5 | Nc6e5   |


    Scenario Outline: Parse a full pgn file
        Given the pgn file <f>
         When we parse it
         Then we should have a full Game that can be stringified to equal the file <g>

        Examples: PGNs
            | f      | g       |
            | f1.pgn | f1.epgn |

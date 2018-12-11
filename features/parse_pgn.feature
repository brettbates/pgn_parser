Feature: Parsing a pgn file

    Scenario Outline: Parse a simple pgn header
        Given a pgn file with only a header of the tag pair <tag_pair>
         When we parse it
         Then we can access a TagPair of k <tp_k>, v <tp_v>

        Examples: Tag Pairs
            | tag_pair                | tp_k  | tp_v        |
            | [Event "Let's Play!"]   | Event | Let's Play! |
            | [Site "Chess.com"]      | Site  | Chess.com   |

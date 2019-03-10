# PGN Parser

A Python library for parsing pgn files into a python friendly format.

The parser is built using (canopy)[http://canopy.jcoglan.com/], the rest is Python.

The PGN spec is based on (and thanks to) the at (saremba.de)[http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm]

## Setup
### Installing

Make sure you have python 3 installed.

```
pip install pgn_parser
```

Then import like so:

```
from pgn_parser import pgn, parser
```


### Testing

For running unit tests (py.test):
```
pytest
```

For running behavioural tests:
```
behave
```


### Building pip distributables

```
make build
```

## Using
### Parsing a pgn file
To parse a pgn, you just give the string to the parser.parse along with the Actions()
which the parser uses to create python structures.
```Python
>>> from pgn_parser import parser, pgn

>>> game = parser.parse("1. e4 e5", actions=pgn.Actions())
>>> print(game.move(1))
1. e4 e5
>>> print(game.move(1).black.san)
e5
```

### Games
After parsing a game, it will be structured into the following classes which are 
nested in eachother:

Game: Container for the whole game
To get a specific move (5 here) from a game
```Python
game.move(5)
```

To retrieve the Movetext
```
game.movetext
```

To access the TagPairs
```
game.tag_pairs
```

To access the final score
```
game.score
```

Movetext: The container of all the moves, e.g "1. c4 c5 2. e4 e5"
It is just a list so can be iterated over to retrieve the moves.
Be warned, Movetext[0] will be the first move parsed, whether 1. or 31. so 
use Game.move() if you want a movenumber

Move: A move is a move number, optionally a white Ply and or a black Ply

Ply: Is the unit of moving, in standard algebraic notation (SAN), 
e.g. the black ply from "1.e4 e5" is e5

TagPairs: An ordered dictionary of all TagPair objects.
These are ordered so it keeps the order read in, but will change to 
seven tag roster order if printed/stringified.


### TagPairs
To store meta data about a game you do so in TagPairs

The header of a pgn file 
```PGN
["Site" "github.com"]
```

Is represented like so in python
```Python
game.tag_pairs["Site'] == "github.com"
```


### Moves
Each move has a move number and two ply's, white and black. 
Each ply can be anything from empty to having comments, variations and 
(nags)[https://en.wikipedia.org/wiki/Numeric_Annotation_Glyphs].

```PGN
moves = "1. e4 $1 {a comment} (1.d5)"
```

Is represented like so:
```Python
m1 = game.move(1)_

assert m1.white.san == "e4"
assert m1.white.comment == "a comment"
assert m1.white.nags[0] == "$1"
assert m1.white.variations[0].move(1).white.san == "d5"
```

If a ply is empty, then its san will be represented "".


### Limitations
No support for RAV style variations
No support for multiple games in one parse, must be single games
Doesn't attempt to parse turn times as this is not in the original spec and I am
not sure what to support.

## Authors

* **Brett Bates** - *Initial work* - (github)[https://github.com/brettbates]

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

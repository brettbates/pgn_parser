import pgn
import re
from collections import OrderedDict

class Actions:
    """Collection of actions for the parser

    Functions that will return the desired structure of a node in the parse tree
    """

    def make_tag_pair(self, input, start, end, elements):
        """Creates dictionary {Key:"Value"} from the parsed tag pair [Key "Value"]"""
        tp = {elements[2].text: elements[5].text}
        return tp

    def make_tag_pairs(self, input, start, end, elements):
        """Creates an ordered dict of collected tag pairs"""
        tps = TagPairs()
        for e in elements:
            k = [k for k in e.keys()][0]
            tps[k] = e[k]
        return tps

    def make_comment(self, input, start, end, elements):
        """Retrieves the comment str without enclosing braces"""
        return elements[1].text.strip('{}')

    def make_movetext(self, input, start, end, elements):
        """Creates the full movetext portion as a List of Move's

        The tree should have all the necessary data parsed to create a list of
        all moves.

        Args:
            elements[x] = A single move = e
            e.move_number = Move number, 1+
            e.white = The SAN of white's move
            e.wcomment = The comment after whites move
            e.black = The SAN of black's move
            e.bcomment = The comment after blacks move

        Returns:
            A List of Move objects in order:
                [Move("1.", "e4", "white comment", "e5", "black comment"), etc]
        """
        mt = []
        for e in elements:
            if type(e.wcomment) == str:
                wcomment = e.wcomment
            else:
                wcomment = ""
            if type(e.bcomment) == str:
                bcomment = e.bcomment
            else:
                bcomment = ""
            mt.append(Move(e.move_number.text,
                           e.white.text,
                           wcomment,
                           e.black.text,
                           bcomment))
        return mt

    def make_game(self, input, start, end, elements):
        """Construct the representation of an entire game

        Args:
            elements = e
            e[0]: Tag Pairs
            e[2]: Movetext
            e[3]: Score

        Returns:
           A Game object, representing a fully parsed pgn file
        """
        e = elements

        if re.match("(1-0|0-1|1/2-1/2|\*)", e[3].text):
            s = Score(e[3].text)
        else:
            s = Score('*')
        g = Game(e[0], e[2], s)
        return g


class TagPairs(OrderedDict):
    """TagPairs is a slightly customised OrderedDict

    It is extended in order to make the __str__ return valid pgn formatted tag pairs
    """

    def __str__(self):
        """Stringify the OrderedDict to a valid Tag Pairs section of a pgn file

        Returns:
           A string with each tag pair represented (in the order it was parsed):
           [Key "Value"]\n
           And an extra newline at the end to begin the movetext section
        """
        out = ""
        for k in self.keys():
            out += '[{} "{}"]\n'.format(k, self[k])

        out += "\n"
        return out


class Ply:
    """A Ply is a half a move in a game, either white or blacks side of the move"""

    def __init__(self, colour, san, comment):
        """Inits the colour san and any comment of the ply"""
        self.colour = colour
        self.san = san
        self.comment = comment

    def __str__(self):
        """Stringifies to a single pgn ply

        Returns:
            <san> {<coment>}
            Ncxe4 {white comment}
        """
        out = self.san
        if self.comment != "":
            out += " {" + self.comment + "}"
        return out


class Move:
    """Representing a move, of 1 or 2 ply along with the move number"""

    def __init__(self, move_number, white, wcomment, black, bcomment):
        """Inits the Move x with the white and or black Ply's"""
        self.move_number = self.move_no_to_i(move_number)
        self.white = Ply("w", white, wcomment)
        self.black = Ply("b", black, bcomment)

    def __str__(self):
        """Stringifies the Move to legal pgn move

        Returns:
            1. e4 e5
        """
        out = "{}.".format(self.move_number)
        out += " {} {}".format(str(self.white), str(self.black))
        return out

    def __repr__(self):
        return self.__str__()

    def move_no_to_i(self, move_number):
        """Turns move number from string to intiger"""
        no = int(re.match("([0-9]+)\.", move_number).groups()[0])
        return no


class Score:
    """Representing the score of a game"""

    def __init__(self, score):
        if score == "*":
            w, b = "*", "*"
        else:
            w, b = score.split('-')
        self.white = w
        self.black = b
        self.result = self.get_result()

    def __str__(self):
        """Stringifies the score to one of the leg possiblities

        Returns:
           1-0, 0-1, 1/2-1/2 or *
        """
        return self.result

    def get_result(self):
        # TODO Perhaps should just be __str__ no need for abstration
        if self.white == "*":
            return "*"
        else:
            return "{}-{}".format(self.white, self.black)


class Game:
    """Represents an entire game

    Attributes:
        tag_pairs: The tag pairs section as an ordered dictionary
        movetext: The List of all Move's
        score: The score of the game
    """

    def __init__(self, tag_pairs, movetext, score):
        """Initialises the Game given the constituent tag_pairs, movetext and score"""
        self.tag_pairs = tag_pairs
        self.movetext = movetext
        self.score = score

    def __str__(self):
        """Stringifies the Game to a valid pgn file"""
        out = str(self.tag_pairs)
        out += self.str_movetext()
        out += str(self.score)
        return out

    def str_movetext(self):
        """Stringifies movetext

        Turns the list of Move's into a valid movetext section

        Returns:
            1. e4 {wc} e5 {bc} 2. d4 {wc2} d5 {bc2}
        """
        out = ""
        for i, m in enumerate(self.movetext):
            out += str(m)
            if i + 1 != len(self.movetext):
               out += "\n"
        out += " "
        return out

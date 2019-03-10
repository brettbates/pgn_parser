import pgn
import re
from collections import OrderedDict, deque

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
        mt = Movetext()
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
                           e.wnags.elements,
                           wcomment,
                           e.wvars,
                           e.black.text,
                           e.bnags.elements,
                           bcomment,
                           e.bvars))
        return mt

    def make_variation(self, input, start, end, elements):
        """Return just the movetext of a variation"""
        return elements[2]

    def make_variations(self, input, start, end, elements):
        """Convert a TreeNode of variations to a List of them"""
        out = []
        for e in elements:
            out.append(e)
        return out

    def make_game(self, input, start, end, elements):
        """Construct the representation of an entire game

        Args:
            elements = e
            e[0]: Tag Pairs
            e[2]: Game Comment
            e[3]: Movetext
            e[4]: Score

        Returns:
           A Game object, representing a fully parsed pgn file
        """
        e = elements

        if re.match("(1-0|0-1|1/2-1/2|\*)", e[4].text):
            s = Score(e[4].text)
        else:
            s = Score('*')
        g = Game(e[0], e[2], e[3], s)
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

        # Seven tag roster list
        strl = ["Event","Site","Date","Round","White","Black","Result"]
        out = ""

        # We first print in order of STR, then any others
        for k in strl:
            if k in self.keys():
                out += '[{} "{}"]\n'.format(k, self[k])

        for k in self.keys():
            if k not in strl:
                out += '[{} "{}"]\n'.format(k, self[k])

        out += "\n"
        return out


class Ply:
    """A Ply is a half a move in a game, either white or blacks side of the move"""

    def __init__(self, colour, san, nags=[], comment="", variations=[]):
        """Inits the colour san and any comment of the ply"""
        self.colour = colour
        self.san = san
        self.nags = self.nodes_to_nags(nags)
        self.comment = comment
        self.variations = variations

    def __str__(self):
        """Stringifies to a single pgn ply

        Returns:
            <san> {<coment>}
            Ncxe4 {white comment}
        """
        out = self.san
        if self.comment != "":
            out += " {" + self.comment.replace('\n', ' ') + "}"
        if len(self.nags) > 0:
            for n in self.nags:
                out += " " + n
        for v in self.variations:
            out += " (" + str(v).strip(' ') + ")"
        return out

    def nodes_to_nags(self, nags):
        """Convert input TreeNode's into a list of string nags"""
        out = []
        for n in nags:
            out.append(n.text.strip(' '))
        return out


class Move:
    """Representing a move, of 1 or 2 ply along with the move number"""

    def __init__(self, move_number, white, wnags, wcomment, wvars, black, bnags, bcomment, bvars):
        """Inits the Move x with the white and or black Ply's"""
        self.move_number = self.move_no_to_i(move_number)
        white = "" if white == ".." else white
        self.white = Ply("w", white, wnags, wcomment, wvars)
        self.black = Ply("b", black, bnags, bcomment, bvars)

    def __str__(self):
        """Stringifies the Move to legal pgn move

        Returns:
            1. e4 e5
        """
        out = "{}.".format(self.move_number)
        if self.white.san != "":
            out += " " + str(self.white)
        else:
            out += ".."
        if self.black.san != "":
            out += " " + str(self.black)
        return out

    def __repr__(self):
        return self.__str__()

    def move_no_to_i(self, move_number):
        """Turns move number from string to intiger"""
        no = int(re.match("([0-9]+)\.", move_number).groups()[0])
        return no


class Movetext(list):
    def __str__(self):
        """Stringifies movetext

        Turns the list of Move's into a valid movetext section

        Returns:
            1. e4 {wc} e5 {bc} 2. d4 {wc2} d5 {bc2}
        """
        out = ""
        for i, m in enumerate(self):
            out += " " + str(m) if i > 0 else str(m)
        out += " "
        return out



class Score:
    """Representing the score of a game"""

    def __init__(self, score):
        if score == "*":
            w, b = "*", "*"
        else:
            w, b = score.split('-')
        self.white = w
        self.black = b
        self.result = str(self)

    def __str__(self):
        """Stringifies the score to one of the leg possiblities

        Returns:
           1-0, 0-1, 1/2-1/2 or *
        """
        if self.white == "*":
            return "*"
        else:
            return "{}-{}".format(self.white, self.black)


class PGNGameException(Exception):
    pass


class Game:
    """Represents an entire game

    Attributes:
        tag_pairs: The tag pairs section as an ordered dictionary
        movetext: The List of all Move's
        score: The score of the game
    """


    def __init__(self, tag_pairs, gcomment, movetext, score):
        """Initialises the Game given the constituent tag_pairs, movetext and score"""
        self.tag_pairs = tag_pairs
        if type(gcomment) == str:
            self.comment = gcomment
        else:
            self.comment = ''
        self.movetext = movetext
        self.score = score

    def __str__(self):
        """Stringifies the Game to a valid pgn file"""
        out = str(self.tag_pairs)
        if self.comment:
            out += "{" + self.comment + "} "
        out += self.format_body()
        return out

    def format_body(self):
        """Keeps the line length to 80 chars on output"""
        mt = deque(str(self.movetext).split(' ') + [])
        out = mt.popleft()
        ll = len(out)
        while True:
            if len(mt) is 0:
                break

            n = mt.popleft()
            # If the current line length + space + character is less than
            # 80 chars long
            if ll + len(n) + 1 < 80:
                to_add = " " + n
                out += " " + n
                ll += len(to_add)
            else:
                out += "\n" + n
                ll = len(n)
        return out + str(self.score)

    def move(self, find):
        """Returns the move number `find`
        Args:
            find: An integer move number

        Returns:
            A Move() object of the requested move number

        Raises:
            PGNGameException is raised if the number cannot be found
        """
        first = self.movetext[0].move_number
        last = self.movetext[-1].move_number
        if first > find:
            raise PGNGameException("Move number {} is not in this game. First is {}, last is {}.".format(find, first, last))

        for m in self.movetext:
            if find == m.move_number:
                return m

        # We haven't found the move
        raise PGNGameException("Move number {} is not in this game. First is {}, last is {}.".format(find, first, last))

import pgn
import re

class Actions:
    def make_tag_pair(self, input, start, end, elements):
        tp = {elements[1].text: elements[3].text}
        return tp

    def make_tag_pairs(self, input, start, end, elements):
        tps = {}
        for e in elements:
            k = [k for k in e.keys()][0]
            tps[k] = e[k]
        return tps

    def make_comment(self, input, start, end, elements):
        return elements[1].text.strip('{}')


    def make_movetext(self, input, start, end, elements):
        mt = []
        for e in elements:
            mt.append(Move(e.move_number.text,
                           e.white.text,
                           e.wcomment,
                           e.black.text,
                           e.bcomment))
        return mt

    def make_game(self, input, start, end, elements):
        import pdb; pdb.set_trace()
        e = [e for e in elements if not (type(e) == pgn.TreeNode and re.match("[\n]", e.text))]

        g = Game(e[0], e[1], Score(e[2].text))
        return g


class Ply:
    def __init__(self, colour, san, comment):
        self.colour = colour
        self.san = san
        self.comment = comment


class Move:
    def __init__(self, move_number, white, wcomment, black, bcomment):
        self.move_number = self.move_no_to_i(move_number)
        self.white = Ply("w", white, wcomment)
        self.black = Ply("b", black, bcomment)

    def __repr__(self):
        return "{}. {} {}".format(self.move_number, self.white.san, self.black.san)

    def move_no_to_i(self, move_number):
        no = int(re.match("([0-9]+)\.", move_number).groups()[0])
        return no


class Score:
    def __init__(self, score):
        if score == "*":
            w, b = "*", "*"
        else:
            w, b = score.split('-')
        self.white = w
        self.black = b
        self.result = self.get_result()

    def get_result(self):
        if self.white == "1":
            return "w"
        elif self.black == "1":
            return "b"
        elif self.white == "1/2":
            return "d"
        else:
            return "*"


class Game:
    def __init__(self, tag_pairs, movetext, score):
        self.tag_pairs = tag_pairs
        self.movetext = movetext
        self.score = score

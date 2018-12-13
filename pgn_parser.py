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

    def make_score(self, input, start, end, elements):
        score = input[start:end]
        if score == "*":
            w, b = "*", "*"
        else:
            w, b = score.split('-')
        return Score(w, b)

    def make_game(self, input, start, end, elements):
        e = elements

        if type(e[3]) == Score:
            s = e[3]
        else:
            s = Score('*', '*')
        g = Game(e[0], e[2], s)
        return g


class Ply:
    def __init__(self, colour, san, comment):
        self.colour = colour
        self.san = san
        self.comment = comment

    def __str__(self):
        return "{}: {} \{{}\}".format(self.colour, self.san, self.comment)


class Move:
    def __init__(self, move_number, white, wcomment, black, bcomment):
        self.move_number = self.move_no_to_i(move_number)
        self.white = Ply("w", white, wcomment)
        self.black = Ply("b", black, bcomment)

    def __str__(self):
        return "{}. {} {}".format(self.move_number, self.white.san, self.black.san)

    def __repr__(self):
        return self.__str__()

    def move_no_to_i(self, move_number):
        no = int(re.match("([0-9]+)\.", move_number).groups()[0])
        return no


class Score:
    def __init__(self, w, b):
        self.white = w
        self.black = b
        self.result = self.get_result()

    def __str__(self):
        return self.result

    def get_result(self):
        if self.white == "*":
            return "*"
        else:
            return "{}-{}".format(self.white, self.black)


class Game:
    def __init__(self, tag_pairs, movetext, score):
        self.tag_pairs = tag_pairs
        self.movetext = movetext
        self.score = score

    def __str__(self):
        out = self.str_tag_pairs()
        out += self.str_movetext()
        out += str(self.score)
        return out

    def str_tag_pairs(self):
        ## TODO Should be in specific order
        return ' '.join(['[{} "{}"]\n'.format(k, self.tag_pairs[k]) for k in self.tag_pairs.keys()]) + "\n"

    def str_movetext(self):
        out = ""
        for m in self.movetext:
            out += str(m)
        out += " "
        return out



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

    def make_score(self, input, start, end, elements):
        score = input[start:end]
        if score == "*":
            w, b = "*", "*"
        else:
            w, b = score.split('-')
        return Score(w, b)

    def make_game(self, input, start, end, elements):
        e = elements

        if re.match("(1-0|0-1|1/2-1/2|\*)", e[3].text):
            s = Score(e[3].text)
        else:
            s = Score('*')
        g = Game(e[0], e[2], s)
        return g


class Ply:
    def __init__(self, colour, san, comment):
        self.colour = colour
        self.san = san
        self.comment = comment

    def __str__(self):
        out = self.san
        if self.comment != "":
            out += " {" + self.comment + "}"
        return out


class Move:
    def __init__(self, move_number, white, wcomment, black, bcomment):
        self.move_number = self.move_no_to_i(move_number)
        self.white = Ply("w", white, wcomment)
        self.black = Ply("b", black, bcomment)

    def __str__(self):
        out = "{}.".format(self.move_number)
        out += " {} {}".format(str(self.white), str(self.black))
        return out

    def __repr__(self):
        return self.__str__()

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
        out = ""
        reqd = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]
        # The Seven Tag Roster in order
        for r in reqd:
            out += '[{} "{}"]\n'.format(r, self.tag_pairs[r])

        # The rest of the the custom tag pairs
        for k in self.tag_pairs.keys():
            if k not in reqd:
                out += '[{} "{}"]\n'.format(k, self.tag_pairs[k])

        out += "\n"
        return out

    def str_movetext(self):
        out = ""
        for i, m in enumerate(self.movetext):
            out += str(m)
            if i + 1 != len(self.movetext):
               out += "\n"
        out += " "
        return out

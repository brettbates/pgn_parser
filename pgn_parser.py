import pgn

class Actions(object):
    def make_comment(self, input, start, end, elements):
        return elements[1].text.strip('{}')

    def make_tag_pair(self, input, start, end, elements):
        tp = {elements[1].text: elements[3].text}
        return tp

    def make_tag_pairs(self, input, start, end, elements):
        tps = {}
        for e in elements:
            k = [k for k in e.keys()][0]
            tps[k] = e[k]
        return tps

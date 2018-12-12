import pgn

class Actions(object):
    def make_comment(self, input, start, end, elements):
        return elements[1].text.strip('{}')

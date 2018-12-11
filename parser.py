#! /usr/bin/env python
# inspired by https://github.com/renatopp/pgnparser

import re


class PgnFile:
    def __init__(self, db_path=None, db_str=None):
        if db_str:
            self.db = [l for l in db_str.split('\n')]
        elif db_path:
            self.db = [l for l in open(db_path)]

        self.tag_pairs = {}

        self.tag_pair_re = re.compile(".*\[([a-zA-Z0-9]+) \"(.*)\"\]")

    def parse(self):
        lines = self.db
        while True:
            token = self._next_token(lines)
            if not token:
                break
            elif token.startswith("["):
                self._parse_tag_pair(token)

    def _next_token(self, lines):
        # Will give the next token, eiter a tag pair or entire movetext
        if lines:
            token = self.db.pop(0)
        else:
            return None

        match_pair = re.match(self.tag_pair_re, token)
        if match_pair:
            return token

        return None

    def _parse_tag_pair(self, token):
        k, v = re.match(self.tag_pair_re, token).groups()
        self.tag_pairs[k] = v

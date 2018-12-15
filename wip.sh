#! /bin/bash

canopy pgn.peg --lang python
behave -kt wip
pytest -m wip

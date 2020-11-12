from typing import Tuple
from .const import levels

class Bridgit:
    def __init__(self, level):
        self.depth = levels[level]

    def handle_move(self, move: Tuple) -> Tuple:
        pass

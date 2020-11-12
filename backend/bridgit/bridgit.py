from typing import Tuple
from .const import levels

class Brigdit:
    def __init__(self, level):
        self.depth = levels[level]

    def handle_move(self, move) -> Tuple:
        pass

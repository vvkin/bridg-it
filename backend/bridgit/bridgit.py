from typing import Tuple
from const import LEVELS, GRID_SIZE, CORNERS
import numpy as np

class Bridgit:
    def __init__(self, level: str, player_num: int):
        self.depth = LEVELS[level]
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), np.int)
        self.player_num = player_num
        self.init_grid()
    
    def init_grid(self):
        for i in range(GRID_SIZE):
            if (i % 2):
                self.grid[i][::2] = 2
            else:
                self.grid[i][1::2] = 1
    
    def is_valid(self, move: Tuple) -> bool:
        return (
            self.grid[move] and move not in CORNERS
                and not (move[0] in (0, GRID_SIZE - 1) and self.player_num != 1)
                and not (move[1] in (0, GRID_SIZE - 1) and self.player_num != 2)
        )
        
    def handle_move(self, move: Tuple) -> Tuple:
        self.grid[move] = self.player_num
        self.make_move()
    
    def make_move(self):
        # find optimal move here
        pass

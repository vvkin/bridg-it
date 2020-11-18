from typing import Tuple
from .const import LEVELS, GRID_SIZE, CORNERS
from .alpha_beta import AlphaBetaPrunning
import numpy as np

class Bridgit:
    def __init__(self, level: str, f_move: bool, color: bool):
        self.f_move = color if f_move else not color
        self.search = AlphaBetaPrunning(LEVELS[level], not self.f_move)
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), np.int)
        self.winner = None
        self.init_grid()
    
    def init_grid(self):
        for i in range(GRID_SIZE):
            if (i % 2):
                self.grid[i][::2] = 2
            else:
                self.grid[i][1::2] = 1
        
        for move in CORNERS:
            self.grid[move] = -1

    def is_valid(self, move: Tuple) -> bool:
        return (
            not self.grid[move] and move not in CORNERS
                and not (move[0] in (0, GRID_SIZE - 1) and not self.f_move)
                and not (move[1] in (0, GRID_SIZE - 1) and self.f_move)
        )
    
    def is_over(self) -> bool:
        return self.winner is not None
    
    def set_move(self, move: Tuple[int, int]) -> None:
        self.grid[move] = (not self.f_move) + 1
        if AlphaBetaPrunning.is_terminal(self.grid, self.f_move):
            self.winner = (not self.f_move) + 1

    def get_move(self) -> Tuple[int, int]:
        self.search(self.grid)
        bot_move = self.search.move
        self.grid[bot_move] = (self.f_move + 1) # update grid
        if AlphaBetaPrunning.is_terminal(self.grid, not self.f_move):
            self.winner = (self.f_move + 1)
        return bot_move

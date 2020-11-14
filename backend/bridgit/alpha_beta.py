import numpy as np
import networkx as nx
from typing import Tuple, List
from const import GRID_SIZE

class AlphaBetaPrunning:
    def __init__(self, depth: int, f_move: bool):
        self.depth = depth
        self.move = self.min if \
            f_move else self.max
    
    @staticmethod
    def is_valid_cell(pos: Tuple[int, int]) -> bool:
        x, y = pos
        return (
            x >= 0 and y >= 0 and
            x < GRID_SIZE and y < GRID_SIZE
        )

    @staticmethod
    def get_neighbors(x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = list(filter(AlphaBetaPrunning.is_valid_cell,
            (
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            )
        ))
        return neighbors

    @staticmethod
    def is_terminal(state: np.ndarray, pos: Tuple[int, int], player_num) -> bool:
        if not np.any(state == 0): return True # tie, there are not any moves

        stack = [(pos[0], pos[1])]
        visited = np.zeros(GRID_SIZE ** 2, np.bool)
        stop_condition = lambda x, y: (
            (y == GRID_SIZE - 1 and player_num) or 
            (x == GRID_SIZE - 1 and not player_num)
        )

        while stack:
            source = stack.pop()
            if stop_condition(*source): 
                return True
            
            neighbors = AlphaBetaPrunning.get_neighbors(*source)
            for (x, y) in neighbors:
                dest = x * 10 + y
                if state[x, y] == player_num + 1 and not visited[dest]:
                    stack.append((x, y))
                    visited[dest] = True

        return False
       
    def init_search(self) -> None:
        self.alpha = np.inf
        self.beta = -np.inf
    
    def __call__(self, state: np.ndarray) -> Tuple[int, int]:
        self.init_search()
        self.state = state
        return self.move(0 ,0)
    
    def max(self, prev, current):
        pass

    def min(self, prev, current):
        pass
import numpy as np
import networkx as nx
from typing import Tuple, List, Generator
from .const import GRID_SIZE

class AlphaBetaPrunning:
    def __init__(self, depth: int, color_idx: bool):
        self.depth = depth
        self.color_idx = color_idx # 1 - "blue", 2 - "red"
        self.move = None
    
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
    def is_terminal(state: np.ndarray, color_idx: bool) -> bool:
        if not np.any(state == 0): return True # tie, there are not any moves

        stop_condition = lambda x, y: (
            (x == GRID_SIZE - 1 and color_idx) or 
            (y == GRID_SIZE - 1 and not color_idx)
        )

        for i in range(GRID_SIZE):
            if color_idx and state[0, i] == 1:
                stack = [(0, i)]
            elif not color_idx and state[i, 0] == 2:
                stack = [(i, 0)]
            else: continue
        
            visited = np.zeros(GRID_SIZE ** 2 + 100, np.bool)
            while stack:
                source = stack.pop()
                if stop_condition(*source): 
                    return True
                
                neighbors = AlphaBetaPrunning.get_neighbors(*source)
                for (x, y) in neighbors:
                    dest = x * 10 + y
                    if state[x, y] == (not color_idx) + 1 and not visited[dest]:
                        stack.append((x, y))
                        visited[dest] = True

        return False
    
    @staticmethod
    def get_chain(state: np.ndarray, move: Tuple[int,int], color_idx: bool) -> List[int]:
        """Return longest chain made by current player"""
        pass

    def get_moves(self, color_idx: bool) -> Generator[Tuple[int, int], None, None]:
        di, dj = not color_idx, color_idx
        for i in range(di, GRID_SIZE - di):
            for j in range(dj, GRID_SIZE - dj):
                if not self.state[i, j]:
                    yield (i, j)

    def heuristic(self) -> float:
        return np.random.rand()
        
    def __call__(self, state: np.ndarray):
        self.state = np.copy(state)
        self.move = None
        self.max(-np.inf, np.inf)

    def update_state(self, move: Tuple[int, int], state_value: int) -> None:
        self.state[move] = state_value
    
    def max(self, alpha, beta, depth=0) -> float:
        if depth > self.depth: return self.heuristic()

        if AlphaBetaPrunning.is_terminal(self.state, not self.color_idx):
            return -1

        minimax = -np.inf
        for move in self.get_moves(self.color_idx): # max player moves first
            self.update_state(move, (not self.color_idx) + 1)
            minimax = max(minimax, self.min(alpha, beta, depth+1))
            self.update_state(move, 0)
            
            if minimax >= beta: return minimax
            if minimax > alpha:
                alpha = minimax
                if not depth: self.move = move
        
        return minimax 
        
    def min(self, alpha, beta, depth=0) -> float:
        if depth > self.depth:
            return -self.heuristic()

        if AlphaBetaPrunning.is_terminal(self.state, self.color_idx):
            return 1
    
        minimax = np.inf
        for move in self.get_moves(not self.color_idx): # min playes moves second
            self.update_state(move, self.color_idx + 1)
            minimax = min(minimax, self.max(alpha, beta, depth+1))
            self.update_state(move, 0)
            
            if minimax <= alpha: return minimax
            beta = min(minimax, beta)

        return minimax
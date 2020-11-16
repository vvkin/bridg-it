import numpy as np
import networkx as nx
from typing import Tuple, List, Generator
from .const import GRID_SIZE

class AlphaBetaPrunning:
    def __init__(self, depth: int, f_move: bool):
        self.depth = depth
        self.move = None
        self.search = self.max if \
            f_move else self.min
    
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
    def is_terminal(state: np.ndarray, f_move: bool) -> bool:
        if not np.any(state == 0): return True # tie, there are not any moves

        stop_condition = lambda x, y: (
            (x == GRID_SIZE - 1 and f_move) or 
            (y == GRID_SIZE - 1 and not f_move)
        )

        for i in range(GRID_SIZE):
            if f_move and state[0, i] == 1:
                stack = [(0, i)]
            elif not f_move and state[i, 0] == 2:
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
                    if state[x, y] == (not f_move) + 1 and not visited[dest]:
                        stack.append((x, y))
                        visited[dest] = True

        return False
    
    @staticmethod
    def get_chain(state: np.ndarray, move: Tuple[int,int], f_move: bool) -> List[int]:
        """Return longest chain made by current player"""
        pass

    def get_moves(self, f_move: bool) -> Generator[Tuple[int, int], None, None]:
        di, dj = not f_move, f_move
        for i in range(di, GRID_SIZE - di):
            for j in range(dj, GRID_SIZE - dj):
                if not self.state[i, j]:
                    yield (i, j)

    def heuristic(self):#, move: Tuple[int, int], f_move: bool) -> float:
        #max_chain = len(AlphaBetaPrunning.get_chain(self.state, 1))
        #min_chain = len(AlphaBetaPrunning.get_chain(self.state, 0))
        #heuristic = 1 / (abs(len(max_chain) - len(min_chain)) + 1)
        #return heuristic if f_move else -heuristic
        return np.random.rand()
        
    def __call__(self, state: np.ndarray):
        self.state = np.copy(state)
        self.move = None

    def update_state(self, move: Tuple[int, int], state_value: int) -> None:
        self.state[move] = state_value
    
    def max(self, alpha, beta, depth=0) -> float:
        if AlphaBetaPrunning.is_terminal(self.state, 0):
            return -1
        
        if depth > self.depth:
            return self.heuristic()
        minimax = -np.inf

        for move in self.get_moves(1): # max player moves first
            self.update_state(move, 1)
            minv = self.min(alpha, beta, depth+1)
            self.update_state(move, 0)

            if minv > minimax:
                minimax = minv
                self.move = move
            
            if minimax >= beta: return minimax
            alpha = max(minimax, alpha)

        return minimax 
        
    def min(self, alpha, beta, depth=0) -> float:
        if depth != 0 and AlphaBetaPrunning.is_terminal(self.state, 1):
            return 1

        if depth > self.depth:
            return -self.heuristic()
        minimax = np.inf

        for move in self.get_moves(0): # min playes moves second
            self.update_state(move, 2)
            maxv = self.max(alpha, beta, depth+1)
            self.update_state(move, 0)

            if maxv < minimax:
                minimax = maxv
                self.move = move
            
            if minimax <= alpha: return minimax
            beta = min(minimax, beta)
        
        return minimax
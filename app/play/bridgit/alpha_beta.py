import numpy as np
from typing import Tuple, List, Generator
from .const import GRID_SIZE
import time

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
    def get_neighbors(move: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = move
        neighbors = ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y))
        return list(filter(AlphaBetaPrunning.is_valid_cell, neighbors))

    @staticmethod
    def stop_condition(move: Tuple[int, int], color_idx: bool, converse: bool):
        dest = 0 if converse else GRID_SIZE - 1
        to_check = move[0] if color_idx else move[1]
        return (to_check == dest)

    @staticmethod
    def is_way(state: np.ndarray, move: Tuple[int, int], converse: bool) -> bool:
        color_idx = not (state[move] - 1) # 0 - blue, 1 - red
        visited = np.zeros((GRID_SIZE, GRID_SIZE), np.bool)
    
        stack = [move]
        while stack:
            source = stack.pop()
            visited[source] = True
            if AlphaBetaPrunning.stop_condition(source, color_idx, converse): 
                return True
            for dest in AlphaBetaPrunning.get_neighbors(source):
                if state[dest] == state[move] and not visited[dest]:
                    stack.append(dest)
        
        return False
    
    @staticmethod
    def is_terminal(state: np.ndarray, move: Tuple[int, int]) -> bool:
        if move is None: return False # first move
        direct = AlphaBetaPrunning.is_way(state, move, True)
        converse = AlphaBetaPrunning.is_way(state, move, False)
        return direct and converse

    def get_moves(self, color_idx: bool) -> Generator[Tuple[int, int], None, None]:
        di, dj = not color_idx, color_idx
        for i in range(di, GRID_SIZE - di):
            for j in range(dj, GRID_SIZE - dj):
                if not self.state[i, j]:
                    yield (i, j)
    
    def heuristic(self, color_idx: bool) -> float:
        multiplier = 1 if color_idx == self.color_idx else -1
        return multiplier * np.random.rand()
             
    def __call__(self, state: np.ndarray):
        self.state = np.copy(state)
        self.move = None
        start = time.time()
        self.max(None, -np.inf, np.inf)
        print(time.time() - start)

    def update_state(self, move: Tuple[int, int], state_value: int) -> None:
        self.state[move] = state_value
    
    def max(self, prev, alpha, beta, depth=0) -> float:
        if depth > self.depth: 
            return self.heuristic(self.color_idx)

        if AlphaBetaPrunning.is_terminal(self.state, prev):
            return -1

        minimax = -np.inf
        for move in self.get_moves(self.color_idx): # max player moves first
            self.update_state(move, (not self.color_idx) + 1)
            minimax = max(minimax, self.min(move, alpha, beta, depth+1))
            self.update_state(move, 0)
            
            if minimax >= beta: return minimax
            if minimax > alpha:
                alpha = minimax
                if not depth: 
                    #print(minimax, move)
                    self.move = move
        
        return minimax 
        
    def min(self, prev, alpha, beta, depth=0) -> float:
        if depth > self.depth:
            return self.heuristic(not self.color_idx)

        if AlphaBetaPrunning.is_terminal(self.state, prev):
            return 1
    
        minimax = np.inf
        for move in self.get_moves(not self.color_idx): # min playes moves second
            self.update_state(move, self.color_idx + 1)
            minimax = min(minimax, self.max(move, alpha, beta, depth+1))
            self.update_state(move, 0)
            
            if minimax <= alpha: return minimax
            beta = min(minimax, beta)

        return minimax
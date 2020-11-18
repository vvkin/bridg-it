import numpy as np
from typing import Tuple, List, Generator
from .const import GRID_SIZE
import time

class AlphaBetaPrunning:
    def __init__(self, depth: int, color_idx: bool):
        self.depth = depth
        self.color_idx = color_idx
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

    def heuristic(self, color_idx: bool) -> float:
        multiplier = 1 if color_idx == self.color_idx else -1
        return multiplier * np.random.rand()
                 
    def get_moves(self, state) -> None:
        blue_moves, red_moves = set(), set()
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if not state[i, j]:
                    if i and i != GRID_SIZE - 1:
                        red_moves.add((i, j))
                    if j and j != GRID_SIZE - 1:
                        blue_moves.add((i, j))

        if self.color_idx: self.moves = blue_moves, red_moves
        else: self.moves = red_moves, blue_moves
    
    def __call__(self, state: np.ndarray):
        self.move = None
        self.get_moves(state)
        start = time.time()
        self.max(state, None, -np.inf, np.inf)
        print(time.time() - start)

    def update_moves(self, move: Tuple[int, int], color_idx: bool, add: bool) -> None:
        if add: self.moves[color_idx].add(move)
        else: self.moves[color_idx].remove(move)
    
    def max(self, state, prev, alpha, beta, depth=0) -> float:
        if depth > self.depth: 
            return self.heuristic(self.color_idx)

        if AlphaBetaPrunning.is_terminal(state, prev):
            return -1
        
        minimax = -np.inf
        for move in self.moves[0]:
            self.update_moves(move, 0, 0)
            state[move] = self.color_idx + 1
            minimax = max(minimax, self.min(state, move, alpha, beta, depth+1))
            self.update_moves(move, 0, 1)
            state[move] = 0
            
            if minimax >= beta: return minimax
            if minimax > alpha:
                alpha = minimax
                if not depth: 
                    print(minimax)
                    self.move = move
        
        return minimax 
        
    def min(self, state, prev, alpha, beta, depth=0) -> float:
        if depth > self.depth:
            return self.heuristic(not self.color_idx)

        if AlphaBetaPrunning.is_terminal(state, prev):
            return 1
        
        minimax = np.inf
        for move in self.moves[1]: # min playes moves second
            self.update_moves(move, 1, 0)
            state[move] = (not self.color_idx) + 1
            minimax = min(minimax, self.max(state, move, alpha, beta, depth+1))
            self.update_moves(move, 1, 1)
            state[move] = 0
           
            if minimax <= alpha: return minimax
            beta = min(minimax, beta)

        return minimax
import numpy as np
from typing import Tuple, List, Generator
from .const import GRID_SIZE

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
    
    @staticmethod
    def get_chain(state: np.ndarray, move: Tuple[int, int], to_search: int) -> int:
        visited = np.zeros((GRID_SIZE, GRID_SIZE), np.bool)
        way = set() # to prevent repetitions

        def DFS(src):
            visited[src] = True
            for dest in AlphaBetaPrunning.get_neighbors(src):
                if state[dest] == to_search and not visited[dest]:
                    way.add(dest[0] if to_search == 1 else dest[1])
                    DFS(dest)
        
        DFS(move)
        return len(way)
    
    @staticmethod
    def get_random_cell(state: np.ndarray, move: Tuple[int, int]):
        while True:
            x = np.random.randint(GRID_SIZE)
            y = np.random.randint(GRID_SIZE)
            if AlphaBetaPrunning.is_valid_cell((x, y)) and \
                (x, y) != move:
                return (x, y)
    
    @staticmethod
    def calculate_chains(state: np.ndarray, move: Tuple[int, int], to_check: int):
        total_length = AlphaBetaPrunning.get_chain(state, move, state[move])
        for _ in range(2):
            cell = AlphaBetaPrunning.get_random_cell(state, move)
            total_length += AlphaBetaPrunning.get_chain(state, cell, to_check)
        return total_length

    def heuristic(self, state: np.ndarray, move: Tuple[int, int]) -> float:
        current = AlphaBetaPrunning.calculate_chains(state, move, state[move])
        opponent = AlphaBetaPrunning.calculate_chains(state, move, 2 if state[move] == 1 else 1)
        return 0.5 if current >= opponent else -0.5
                 
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
        self.max(state, None, -np.inf, np.inf)

    def update_moves(self, move: Tuple[int, int], color_idx: bool, add: bool) -> None:
        if add: self.moves[color_idx].add(move)
        else: self.moves[color_idx].remove(move)
    
    def max(self, state, prev, alpha, beta, depth=0) -> float:
        if depth >= self.depth: 
            return self.heuristic(state, prev)

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
                if not depth: self.move = move
                alpha = minimax
                
        return minimax 
        
    def min(self, state, prev, alpha, beta, depth=0) -> float:
        if depth >= self.depth:
            return self.heuristic(state, prev)

        if AlphaBetaPrunning.is_terminal(state, prev):
            return 1
        
        minimax = np.inf
        for move in self.moves[1]:
            self.update_moves(move, 1, 0)
            state[move] = (not self.color_idx) + 1
            minimax = min(minimax, self.max(state, move, alpha, beta, depth+1))
            self.update_moves(move, 1, 1)
            state[move] = 0
           
            if minimax <= alpha: return minimax
            beta = min(minimax, beta)

        return minimax
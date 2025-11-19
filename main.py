from collections import deque
from typing import List, Tuple, Optional
import copy

class SolitaireSolver:
    CARD_ORDER = [14, 13, 12, 11, 10, 9, 8, 7, 6]  # T, K, D, V, 10, 9, 8, 7, 6
    
    def __init__(self, board: List[List[int]]):
        """
        Initialize solver with board configuration.
        board: List of stacks, each stack is a list of cards (bottom to top)
        """
        self.initial_board = [stack[:] for stack in board]
    
    def is_valid_stack(self, stack: List[int]) -> bool:
        """Check if a stack follows the decreasing order rule."""
        if not stack:
            return True
        for i in range(len(stack) - 1):
            if stack[i] not in self.CARD_ORDER or stack[i+1] not in self.CARD_ORDER:
                return False
            if self.CARD_ORDER.index(stack[i]) + 1 != self.CARD_ORDER.index(stack[i+1]):
                return False
        return True
    
    def is_complete_stack(self, stack: List[int]) -> bool:
        """Check if a stack is complete (T to 6)."""
        return (len(stack) == 9 and 
                stack == self.CARD_ORDER)
    
    def can_place_on(self, card: int, target_stack: List[int]) -> bool:
        """Check if a card can be placed on target stack."""
        if not target_stack:
            return True
        top_card = target_stack[-1]
        if top_card not in self.CARD_ORDER or card not in self.CARD_ORDER:
            return False
        return self.CARD_ORDER.index(top_card) == self.CARD_ORDER.index(card) + 1
    
    def remove_complete_stacks(self, board: List[List[int]]) -> List[List[int]]:
        """Remove any complete stacks from the board."""
        new_board = []
        for stack in board:
            if not self.is_complete_stack(stack):
                new_board.append(stack[:])
        return new_board
    
    def get_movable_sequence(self, stack: List[int]) -> int:
        """Get the number of cards that can be moved as a valid sequence from top."""
        if not stack:
            return 0
        count = 1
        for i in range(len(stack) - 1, 0, -1):
            if (stack[i] in self.CARD_ORDER and stack[i-1] in self.CARD_ORDER and
                self.CARD_ORDER.index(stack[i-1]) + 1 == self.CARD_ORDER.index(stack[i])):
                count += 1
            else:
                break
        return count
    
    def board_to_tuple(self, board: List[List[int]]) -> tuple:
        """Convert board to hashable tuple for state tracking."""
        return tuple(tuple(stack) for stack in board)
    
    def solve_without_cheating(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Solve the puzzle without using invalid positions (no cheating).
        Returns list of moves as (from_stack, to_stack, num_cards) or None if impossible.
        """
        queue = deque([(self.initial_board, [])])
        visited = {self.board_to_tuple(self.initial_board)}
        
        while queue:
            board, moves = queue.popleft()
            
            board = self.remove_complete_stacks(board)
            
            if all(len(stack) == 0 for stack in board):
                return moves
            
            for from_idx in range(len(board)):
                if not board[from_idx]:
                    continue
                
                movable = self.get_movable_sequence(board[from_idx])
                
                for amount in range(1, movable + 1):
                    cards_to_move = board[from_idx][-amount:]
                    
                    for to_idx in range(len(board)):
                        if from_idx == to_idx:
                            continue
                        
                        if self.can_place_on(cards_to_move[0], board[to_idx]):
                            new_board = [stack[:] for stack in board]
                            new_board[from_idx] = new_board[from_idx][:-amount]
                            new_board[to_idx] = new_board[to_idx] + cards_to_move
                            
                            board_tuple = self.board_to_tuple(new_board)
                            if board_tuple not in visited:
                                visited.add(board_tuple)
                                new_moves = moves + [(from_idx, to_idx, amount)]
                                queue.append((new_board, new_moves))
        
        return None
    
    def solve_with_cheating(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Solve allowing single card moves to invalid positions.
        Returns list of moves as (from_stack, to_stack, num_cards) or None if impossible.
        """
        queue = deque([(self.initial_board, [])])
        visited = {self.board_to_tuple(self.initial_board)}
        max_iterations = 100000
        iterations = 0
        
        while queue and iterations < max_iterations:
            iterations += 1
            board, moves = queue.popleft()
            
            board = self.remove_complete_stacks(board)
            
            if all(len(stack) == 0 for stack in board):
                return moves
            
            for from_idx in range(len(board)):
                if not board[from_idx]:
                    continue
                
                top_card = board[from_idx][-1]
                from_invalid = not self.is_valid_stack(board[from_idx])
                
                if from_invalid:
                    for to_idx in range(len(board)):
                        if from_idx == to_idx:
                            continue
                        
                        if self.can_place_on(top_card, board[to_idx]):
                            new_board = [stack[:] for stack in board]
                            new_board[from_idx] = new_board[from_idx][:-1]
                            new_board[to_idx] = new_board[to_idx] + [top_card]
                            
                            board_tuple = self.board_to_tuple(new_board)
                            if board_tuple not in visited:
                                visited.add(board_tuple)
                                new_moves = moves + [(from_idx, to_idx, 1)]
                                queue.append((new_board, new_moves))
                else:
                    movable = self.get_movable_sequence(board[from_idx])
                    
                    for amount in range(1, movable + 1):
                        cards_to_move = board[from_idx][-amount:]
                        
                        for to_idx in range(len(board)):
                            if from_idx == to_idx:
                                continue
                            
                            if board[to_idx] and not self.is_valid_stack(board[to_idx]):
                                continue
                            
                            if amount > 1 or self.can_place_on(cards_to_move[0], board[to_idx]):
                                valid_move = self.can_place_on(cards_to_move[0], board[to_idx])
                                
                                new_board = [stack[:] for stack in board]
                                new_board[from_idx] = new_board[from_idx][:-amount]
                                new_board[to_idx] = new_board[to_idx] + cards_to_move
                                
                                if amount == 1 and not valid_move:
                                    if not self.is_valid_stack(board[to_idx]):
                                        continue
                                
                                board_tuple = self.board_to_tuple(new_board)
                                if board_tuple not in visited:
                                    visited.add(board_tuple)
                                    new_moves = moves + [(from_idx, to_idx, amount)]
                                    queue.append((new_board, new_moves))
        
        return None
    
    def solve(self, allow_cheating: bool = True) -> Optional[List[Tuple[int, int, int]]]:
        """
        Main solve method.
        Returns list of moves or None if impossible.
        """
        solution = self.solve_without_cheating()
        if solution is not None:
            return solution
        
        if allow_cheating:
            return self.solve_with_cheating()
        
        return None


if __name__ == "__main__":
    # Example board from the image (top-left)
    # Stack indices: 0, 1, 2, 3 (left to right)
    board1 = [
        [13, 11, 10, 9, 8, 7],  # K, V, 10, 9, 8, 7
        [14],                    # T
        [10, 9, 8, 7, 6],       # 10, 9, 8, 7, 6
        []                       # Empty
    ]
    
    solver1 = SolitaireSolver(board1)
    solution1 = solver1.solve(allow_cheating=False)
    
    if solution1:
        print("Solution found (no cheating):")
        for move in solution1:
            print(f"  Move {move[2]} card(s) from stack {move[0]} to stack {move[1]}")
    else:
        print("No solution without cheating")
        solution1_cheat = solver1.solve(allow_cheating=True)
        if solution1_cheat:
            print("Solution found (with cheating):")
            for move in solution1_cheat:
                print(f"  Move {move[2]} card(s) from stack {move[0]} to stack {move[1]}")
        else:
            print("No solution possible")
    
    print("\n" + "="*50)
    board2 = [
        [14, 13, 12, 11, 10, 9, 8, 7],
        [6],
        [],
        []
    ]
    
    solver2 = SolitaireSolver(board2)
    solution2 = solver2.solve(allow_cheating=False)
    
    if solution2:
        print("Simple test - Solution found:")
        for move in solution2:
            print(f"  Move {move[2]} card(s) from stack {move[0]} to stack {move[1]}")
    else:
        print("Simple test - No solution")
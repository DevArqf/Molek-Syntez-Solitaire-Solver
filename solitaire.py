from collections import deque
from typing import List, Tuple, Optional

class SolitaireSolver:
    CARD_ORDER = [14, 13, 12, 11, 10, 9, 8, 7, 6]
    CARD_NAMES = {14: 'T', 13: 'K', 12: 'D', 11: 'V', 10: '10', 9: '9', 8: '8', 7: '7', 6: '6'}
    
    def __init__(self, board: List[List[int]]):
        self.initial_board = [stack[:] for stack in board]
    
    def print_board(self, board: List[List[int]], title: str = "Board"):
        print(f"\n{title}:")
        max_height = max(len(stack) for stack in board) if board else 0
        
        for level in range(max_height - 1, -1, -1):
            row = ""
            for stack in board:
                if level < len(stack):
                    row += f" {self.CARD_NAMES[stack[level]]:>3} "
                else:
                    row += "     "
            print(row)
        
        print("  " + "  ".join(f"[{i}]" for i in range(len(board))))
        print()
    
    def is_valid_stack(self, stack: List[int]) -> bool:
        if not stack:
            return True
        for i in range(len(stack) - 1):
            if stack[i] not in self.CARD_ORDER or stack[i+1] not in self.CARD_ORDER:
                return False
            if self.CARD_ORDER.index(stack[i]) + 1 != self.CARD_ORDER.index(stack[i+1]):
                return False
        return True
    
    def is_complete_stack(self, stack: List[int]) -> bool:
        return len(stack) == 9 and stack == self.CARD_ORDER
    
    def can_place_on(self, card: int, target_stack: List[int]) -> bool:
        if not target_stack:
            return True
        top_card = target_stack[-1]
        if top_card not in self.CARD_ORDER or card not in self.CARD_ORDER:
            return False
        return self.CARD_ORDER.index(top_card) == self.CARD_ORDER.index(card) - 1
    
    def remove_complete_stacks(self, board: List[List[int]], verbose: bool = False) -> List[List[int]]:
        new_board = []
        for stack in board:
            if self.is_complete_stack(stack):
                if verbose:
                    print(f"  ✓ Complete stack removed: {[self.CARD_NAMES[c] for c in stack]}")
        #        new_board.append([]) # this removes the column entirely. Not an ideal solution - I'd prefer it if the stack remained but was not interactable, or if there were an indicator that there was a complete stack in the slot. However, that's beyond my limited python knowledge
            else:
                new_board.append(stack[:])
        return new_board
    
    def get_movable_sequence(self, stack: List[int]) -> int:
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
        return tuple(tuple(stack) for stack in board)
    
    def solve_without_cheating(self) -> Optional[List[Tuple[int, int, int]]]:
        queue = deque([(self.initial_board, [])])
        visited = {self.board_to_tuple(self.initial_board)}
        
        while queue:
            board, moves = queue.popleft()
            board = self.remove_complete_stacks(board)
            
            if all(self.is_complete_stack(stack) or len(stack) == 0 for stack in board): # an alternate solution I was exploring. No longer necessary, but doesn't seem to hurt anything, and is a little more robust
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
    
    def solve(self, allow_cheating: bool = True) -> Optional[List[Tuple[int, int, int]]]:
        solution = self.solve_without_cheating()
        if solution is not None:
            return solution
        return None
    
    def visualize_solution(self, solution: Optional[List[Tuple[int, int, int]]]):
        if solution is None:
            print("❌ No solution found!")
            return
        
        print(f"✅ Solution found in {len(solution)} moves!\n")
        board = [stack[:] for stack in self.initial_board]
        self.print_board(board, "Initial Board")
        
        for step, (from_idx, to_idx, amount) in enumerate(solution, 1):
            cards = board[from_idx][-amount:]
            board[from_idx] = board[from_idx][:-amount]
            board[to_idx] = board[to_idx] + cards
            
            card_names = [self.CARD_NAMES[c] for c in cards]
            print(f"Step {step}: Move {card_names} (x{amount}) from stack {from_idx} to stack {to_idx}")
            
            board = self.remove_complete_stacks(board, verbose=True)
            self.print_board(board, f"After Step {step}")
        
        if all(self.is_complete_stack(stack) or len(stack) == 0 for stack in board): # see line 82 for explanation
            print("🎉 PUZZLE SOLVED! All stacks cleared!")
        else:
            print("⚠️ Warning: Board not fully cleared")


def run_tests():
    print("="*60)
    print("TEST 1: Simple Completion Test")
    print("="*60)
    board1 = [
        [14, 13, 12, 11, 10, 9, 8, 7],
        [6],
        [],
        []
    ]
    solver1 = SolitaireSolver(board1)
    solution1 = solver1.solve()
    solver1.visualize_solution(solution1)
    
    print("\n" + "="*60)
    print("TEST 2: Two-Move Solution")
    print("="*60)
    board2 = [
        [14, 13],
        [12, 11, 10, 9, 8, 7, 6],
        [],
        []
    ]
    solver2 = SolitaireSolver(board2)
    solution2 = solver2.solve()
    solver2.visualize_solution(solution2)
    
    print("\n" + "="*60)
    print("TEST 3: Complex Rearrangement")
    print("="*60)
    board3 = [
        [14],
        [13, 12, 11],
        [10, 9, 8, 7, 6],
        []
    ]
    solver3 = SolitaireSolver(board3)
    solution3 = solver3.solve()
    solver3.visualize_solution(solution3)
    
    print("\n" + "="*60)
    print("TEST 4: Empty Board (Already Solved)")
    print("="*60)
    board4 = [[], [], [], []]
    solver4 = SolitaireSolver(board4)
    solution4 = solver4.solve()
    solver4.visualize_solution(solution4)
    
    print("\n" + "="*60)
    print("TEST 5: Impossible Board")
    print("="*60)
    board5 = [
        [14, 13, 12],
        [11, 10],
        [],
        []
    ]
    solver5 = SolitaireSolver(board5)
    solution5 = solver5.solve()
    solver5.visualize_solution(solution5)


def interactive_mode():
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("\nEnter your board configuration.")
    print("Card values: T=14, K=13, D=12, V=11, 10=10, 9=9, 8=8, 7=7, 6=6")
    print("Enter each stack as comma-separated numbers")
    print("Enter empty line for empty stack. Type 'done' when finished.\n")
    
    board = []
    stack_num = 0
    
    while True:
        user_input = input(f"Stack {stack_num} (or 'done'): ").strip()
        
        if user_input.lower() == 'done':
            break
        
        if user_input == '':
            board.append([])
        else:
            try:
                stack = [int(x.strip()) for x in user_input.split(',')]
                board.append(stack)
            except ValueError:
                print("Invalid input. Please enter comma-separated numbers.")
                continue
        
        stack_num += 1
    
    if not board:
        print("No board entered.")
        return
    
    solver = SolitaireSolver(board)
    solution = solver.solve()
    solver.visualize_solution(solution)


if __name__ == "__main__":
    print("🎴 MOLEK-SYNTEZ SOLITAIRE SOLVER 🎴\n")
    
    run_tests()
    
    # Uncomment to enable interactive mode
    # interactive_mode()


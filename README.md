# Molek-Syntez Solitaire Solver

A Python solver for the solitaire minigame from Zachtronics' "Molek-Syntez" made as a learning project. The solver uses breadth-first search to find optimal solutions for card-stacking puzzles.

## About the Game

In this solitaire variant, cards must be stacked in a specific decreasing order: T (14), K (13), D (12), V (11), 10, 9, 8, 7, 6. When you complete a full sequence of all nine cards, the stack automatically disappears. The goal is to clear all cards from the board.

The rules are straightforward but the puzzles can be tricky. You can only move cards that form valid sequences, and they can only be placed on the next card in the sequence. For example, you can place a 7 on an 8, or a 10 on a V (11).

## How It Works

The solver explores all possible moves using a breadth-first search algorithm. It systematically tries every legal move, keeping track of board states it has already seen to avoid redundant work. When it finds a sequence of moves that clears the board, it returns that solution.

The algorithm guarantees finding the shortest possible solution if one exists. If the puzzle is impossible to solve, it will tell you that too.

## Installation

No external dependencies required. Just Python 3.6 or higher.
```bash
git clone https://github.com/yourusername/Molek-Syntez-Solitaire-Solver.git
cd Molek-Syntez-Solitaire-Solver
python solitaire.py
```

## Usage

Run the script to see the built-in test cases:
```bash
python solitaire.py
```

This will run through five different puzzles and show you the solutions step by step.

### Using the Solver in Your Code
```python
from solitaire import SolitaireSolver

# Define your board as a list of stacks
# Each stack is a list of cards from bottom to top
board = [
    [14, 13, 12, 11, 10, 9, 8, 7],  # Stack 0
    [6],                             # Stack 1
    [],                              # Stack 2 (empty)
    []                               # Stack 3 (empty)
]

solver = SolitaireSolver(board)
solution = solver.solve()

if solution:
    solver.visualize_solution(solution)
else:
    print("No solution exists for this board")
```

### Interactive Mode

You can also solve custom boards interactively. Uncomment the last line in the main section:
```python
if __name__ == "__main__":
    print("🎴 MOLEK-SYNTEZ SOLITAIRE SOLVER 🎴\n")
    
    run_tests()
    interactive_mode()  # Uncomment this line
```

Then run the script and enter your board configuration when prompted.

## Example Output
```
Initial Board:
   7
   8
   9
  10
   V
   D
   K
   T    6
  [0]  [1]  [2]  [3]

Solution found in 1 moves!

Step 1: Move ['6'] (x1) from stack 1 to stack 0
  Complete stack removed: ['T', 'K', 'D', 'V', '10', '9', '8', '7', '6']

PUZZLE SOLVED! All stacks cleared!
```

## Project Structure
```
Molek-Syntez-Solitaire-Solver/
├── LICENSE
├── README.md
└── solitaire.py
```

## Acknowledgments

This project was inspired by the solitaire minigame in Zachtronics' "Molek-Syntez". The game mechanics and card order are based on that implementation.

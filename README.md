# **AI-Futoshiki**

## **Overview**
This project implements an AI-based solver for the Futoshiki puzzle. The puzzle involves placing numbers on a grid while satisfying given inequalities between cells. The program supports input parsing, solving puzzles using backtracking with forward checking, and providing runtime statistics.

## **Features**
- Handles Futoshiki puzzles with any size up to 9x9.
- Implements backtracking with forward checking to enforce constraints.
- Supports command-line inputs or batch processing of puzzles from a file.
- Outputs runtime statistics including mean, min, max, and standard deviation of runtimes.

## **How the Board Works**
- The board is represented as a dictionary with string keys and integer values.
  - **Variables**: Each cell is identified by a row and column (e.g., `A1`).
  - **Empty Cells**: Represented by `0`.
  - **Inequalities**:
    - `A*1 = '<'` means the value at `A1` must be less than the value at `B1`.
    - `A1* = '>'` means the value at `A1` is greater than the value at `A2`.
  - **Empty Inequalities**: Represented by `'-'`

## **Installation**
Clone the repository:
```bash
git clone https://github.com/yourusername/ai-futoshiki.git
cd ai-futoshiki

Solve a Single Puzzle: Provide a configuration string as input:
python futoshiki.py <config_string>

Batch Solve Puzzles: Place multiple configuration strings in a file (futoshiki_start.txt) and run:
python futoshiki.py


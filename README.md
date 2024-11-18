# **AI-Futoshiki**

## **Overview**
This project is an AI-based solver for the Futoshiki puzzle, a logic puzzle that involves placing numbers on a grid while adhering to given constraints. The program uses advanced algorithms to solve puzzles efficiently while providing runtime statistics.

## **Features**
- Solves Futoshiki puzzles of various sizes and complexities.
- Implements backtracking with optimizations like Minimum Remaining Value (MRV) and forward checking.
- Reports runtime statistics, including the number of iterations and backtracks.
- Flexible design to accommodate puzzles with custom constraints.

## **Project Structure**
Here’s a breakdown of the key files:

- **`FutoshikiSolver.py`**: Core logic for solving Futoshiki puzzles using backtracking and heuristics.
- **`ConstraintChecker.py`**: Validates constraints during the solving process.
- **`PuzzleParser.py`**: Parses puzzle inputs from files or user input.
- **`StatisticsCollector.py`**: Tracks runtime performance and outputs statistics.
- **`README.md`**: Documentation for the project (this file).

## **Installation**
Clone the repository:
```bash
git clone https://github.com/yourusername/ai-futoshiki.git
cd ai-futoshiki
run using python FutoshikiSolver.py --input puzzle.txt
# Puzzles

A repo containing code to solve Sudokos and the like.

To solve a sudoku first import the `Sudoku` class.

```python
from puzzles.sudoku import Sudoku
```

Define your puzzle input. This should simply be a grid where any unknown
squares are filled in with a `0`.

```python
P = [[0, 7, 0, 4, 0, 0, 0, 9, 2],
     [0, 0, 0, 0, 8, 0, 0, 0, 5],
     [0, 0, 3, 0, 0, 0, 7, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 8, 0],
     [0, 0, 7, 0, 1, 0, 5, 0, 4],
     [0, 0, 0, 2, 3, 7, 0, 0, 0],
     [2, 0, 4, 0, 0, 5, 0, 0, 3],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [8, 0, 5, 0, 0, 0, 1, 0, 0]]
```

Then run the following to get a solution!
```python
solver = Sudoku(P)
solution = solver.solve()
```

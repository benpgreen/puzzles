import numpy as np
import itertools


def _sudoku_is_valid(S):
    """Checks if sudoku is valid."""

    S = np.array(S)
    output = True
    for i in range(9):
        rel = S[i]
        rel = rel[rel > 0]
        if len(np.unique(rel)) != len(rel):
            output = False
            break
    if output:
        for i in range(9):
            rel = S[:, i]
            rel = rel[rel > 0]
            if len(np.unique(rel)) != len(rel):
                output = False
                break
    if output:
        for i, j in itertools.product((0, 3, 6), (0, 3, 6)):
            square = S[i:i+3, j:j+3].flatten()
            rel = square[square > 0]
            if len(np.unique(rel)) != len(rel):
                output = False
                break
    return output


def _sixdoku_is_valid(S):
    """Checks if sixdoku is valid."""

    S = np.array(S)
    output = True
    for i in range(6):
        rel = S[i]
        rel = rel[rel > 0]
        if len(np.unique(rel)) != len(rel):
            output = False
            break
    if output:
        for i in range(6):
            rel = S[:, i]
            rel = rel[rel > 0]
            if len(np.unique(rel)) != len(rel):
                output = False
                break
    if output:
        for i, j in itertools.product((0, 2, 4), (0, 3)):
            square = S[i:i+2, j:j+3].flatten()
            rel = square[square > 0]
            if len(np.unique(rel)) != len(rel):
                output = False
                break
    return output


class Sudoku:

    def __init__(self, puzzle):
        P = np.array(puzzle)
        numbers = [i for i in range(9)]
        possible_entries = {}
        count_to_pos = {}
        counter = 0
        for i, j in itertools.product(numbers, numbers):
            if P[i, j] == 0:
                # next number to check, current puzzle
                possible_entries[counter] = [1, None]
                count_to_pos[counter] = (i, j)
                counter += 1
        self.puzzle = P
        self._possible_entries = possible_entries
        self._count_to_pos = count_to_pos
        self._count = counter

    def solve(self):
        i = 0
        S = self.puzzle.copy()
        possible_entries = self._possible_entries
        while i < self._count:
            num, _ = possible_entries[i]
            x, y = self._count_to_pos[i]
            while num < 10:
                S[x, y] = num
                if _sudoku_is_valid(S):
                    break
                num += 1
            if num < 10:
                possible_entries[i] = [num + 1, S.copy()]
                i += 1
            else:
                possible_entries[i] = [1, None]
                i += -1
                S = possible_entries[i][1].copy()

        solution = possible_entries[self._count-1][1]
        self.solution = solution
        return solution


class Sixdoku:

    def __init__(self, puzzle):
        P = np.array(puzzle)
        numbers = [i for i in range(6)]
        possible_entries = {}
        count_to_pos = {}
        counter = 0
        for i, j in itertools.product(numbers, numbers):
            if P[i, j] == 0:
                # next number to check, current puzzle
                possible_entries[counter] = [1, None]
                count_to_pos[counter] = (i, j)
                counter += 1
        self.puzzle = P
        self._possible_entries = possible_entries
        self._count_to_pos = count_to_pos
        self._count = counter

    def solve(self):
        i = 0
        S = self.puzzle.copy()
        possible_entries = self._possible_entries
        while i < self._count:
            num, _ = possible_entries[i]
            x, y = self._count_to_pos[i]
            while num < 7:
                S[x, y] = num
                if _sixdoku_is_valid(S):
                    break
                num += 1
            if num < 7:
                possible_entries[i] = [num + 1, S.copy()]
                i += 1
            else:
                possible_entries[i] = [1, None]
                i += -1
                S = possible_entries[i][1].copy()

        solution = possible_entries[self._count-1][1]
        self.solution = solution
        return solution

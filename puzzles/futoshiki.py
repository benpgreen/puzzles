import numpy as np
import itertools


def _is_valid(S, relations):

    S = np.array(S)
    n = len(S)
    output = True
    for i in range(n):
        rel = S[i]
        rel = rel[rel > 0]
        if len(np.unique(rel)) != len(rel):
            output = False
            break
    if output:
        for i in range(n):
            rel = S[:, i]
            rel = rel[rel > 0]
            if len(np.unique(rel)) != len(rel):
                output = False
                break
    if output:
        for relation in relations:
            if S[relation[0]] != 0 and S[relation[1]] != 0:
                if S[relation[0]] >= S[relation[1]]:
                    output = False
                    break

    return output


class Futoshiki:

    def __init__(self, puzzle):
        # get input data
        i = 0
        P = []
        relations = []
        for row in puzzle:
            p = []
            j = 0
            if isinstance(row[0], int):
                # a numbers row...
                for val in row:
                    if isinstance(val, int):
                        p.append(val)
                        j += 1
                    elif val == '<':
                        relations.append([(i, j-1), (i, j)])
                    elif val == '>':
                        relations.append([(i, j), (i, j-1)])
                P.append(p)
                i += 1
            else:
                # a relations row...
                for val in row:
                    if val == '<':
                        relations.append([(i-1, j), (i, j)])
                    elif val == '>':
                        relations.append([(i, j), (i-1, j)])
                    j += 1

        P = np.array(P)
        n = len(P)
        self.size = n

        numbers = [i for i in range(n)]
        possible_entries = {}
        count_to_pos = {}
        counter = 0
        for i, j in itertools.product(numbers, numbers):
            if P[i, j] == 0:
                # next number to check, current puzzle
                possible_entries[counter] = [1, None]
                count_to_pos[counter] = (i, j)
                counter += 1
        self.puzzle_grid = P
        self.puzzle_relations = relations
        self._possible_entries = possible_entries
        self._count_to_pos = count_to_pos
        self._count = counter

    def solve(self):
        i = 0
        S = self.puzzle_grid.copy()
        possible_entries = self._possible_entries
        relations = self.puzzle_relations
        n = self.size
        while i < self._count:
            num, _ = possible_entries[i]
            x, y = self._count_to_pos[i]
            while num <= n:
                S[x, y] = num
                if _is_valid(S, relations):
                    break
                num += 1
            if num <= n:
                possible_entries[i] = [num + 1, S.copy()]
                i += 1
            else:
                possible_entries[i] = [1, None]
                i += -1
                S = possible_entries[i][1].copy()

        solution = possible_entries[self._count-1][1]
        self.solution = solution
        return solution

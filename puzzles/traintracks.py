import numpy as np
import itertools

test = {
    "tracks": [(5, 0, "#"), (2, 4, "#"), (5, 5, "#")],
    "x": [3, 6, 5, 1, 3, 6],
    "y": [5, 3, 4, 4, 4, 4]
}


class TrainTrack:

    def __init__(self, x, y, track_locations):
        self.x = np.array(x)
        self.y = np.array(y)

        X = len(x)
        Y = len(y)
        self.track = np.array([["" for _ in range(Y)] for __ in range(X)])

        for i, j, entry in track_locations:
            self.track[i, j] = entry

        self.options = [".", "#"]

        possible_entries = {}
        count_to_pos = {}
        counter = 0
        for i, j in itertools.product(range(X), range(Y)):
            if self.track[i, j] == "":
                # next number to check, current puzzle
                possible_entries[counter] = [0, None]
                count_to_pos[counter] = (i, j)
                counter += 1
        self._possible_entries = possible_entries
        self._count_to_pos = count_to_pos
        self._count = counter

    def _is_valid(self, T):
        output = True
        if ((T == "#").sum(axis=0) > self.x).any():
            output = False
        elif ((T != ".").sum(axis=0) < self.x).any():
            output = False
        elif ((T == "#").sum(axis=1) > self.y).any():
            output = False
        elif ((T != ".").sum(axis=1) < self.y).any():
            output = False
        return output

    def solve(self):
        i = 0
        T = self.track.copy()
        possible_entries = self._possible_entries
        while i < self._count:
            idx = possible_entries[i][0]
            x, y = self._count_to_pos[i]
            while idx < len(self.options):
                T[x, y] = self.options[idx]
                if self._is_valid(T):
                    break
                idx += 1
            if idx < len(self.options):
                possible_entries[i] = [idx + 1, T.copy()]
                i += 1
            else:
                possible_entries[i] = [0, None]
                i += -1
                T = possible_entries[i][1].copy()

        solution = possible_entries[self._count - 1][1]
        self.solution = solution
        return solution

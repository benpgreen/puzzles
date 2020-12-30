import numpy as np
import itertools

from tqdm import tqdm


TRACK_SE = "\u250c"
TRACK_SW = "\u2510"
TRACK_NE = "\u2514"
TRACK_NW = "\u2518"


test = {
    "tracks": [(5, 0, "-"), (2, 4, TRACK_SE), (5, 5, "|")],
    "x": [3, 6, 5, 1, 3, 6],
    "y": [5, 3, 4, 4, 4, 4]
}

simple = {
    "tracks": [(0, 3, "-"), (3, 0, "-")],
    "x": [3, 4, 3, 1],
    "y": [3, 2, 3, 3]
}

really_simple = {
    "tracks": [(2, 0, "-"), (0, 1, TRACK_NW)],
    "x": [3, 3, 2],
    "y": [2, 3, 3]
}

full_track = [
    (2, 0, "-"), (2, 1, "-"), (2, 2, TRACK_NW),
    (1, 2, TRACK_SW), (1, 1, "-"), (1, 0, TRACK_NE),
    (0, 0, TRACK_SE), (0, 1, TRACK_NW)
]


class TrainTrack:

    def __init__(self, x=None, y=None, track_locations=None, dict=None):
        if dict is not None:
            x = dict["x"]
            y = dict["y"]
            track_locations = dict["tracks"]

        self.x = np.array(x)
        self.y = np.array(y)

        X = len(x)
        Y = len(y)
        self.track = np.array([["" for _ in range(Y)] for __ in range(X)])

        ends = []
        for i, j, entry in track_locations:
            self.track[i, j] = entry
            if i == 0 and entry in ("|", TRACK_NE, TRACK_NW):
                ends.append((i, j, "S"))
            elif i == X - 1 and entry in ("|", TRACK_SE, TRACK_SW):
                ends.append((i, j, "N"))
            elif j == 0 and entry in ("-", TRACK_NW, TRACK_SW):
                ends.append((i, j, "E"))
            elif j == Y - 1 and entry in ("-", TRACK_NE, TRACK_SE):
                ends.append((i, j, "W"))
        if len(ends) != 2:
            raise ValueError(f"{len(ends)} ends found: {ends}")
        self.start = ends[0]
        self.end = (ends[1][0], ends[1][1])

        self.options = [".", "-", "|", TRACK_NE, TRACK_NW, TRACK_SE, TRACK_SW]

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

    def _is_path(self, T):
        i, j, direction = self.start
        path = {(i, j)}
        output = True

        while (i, j) != self.end and output:

            if direction == "E":
                j += 1
            elif direction == "W":
                j -= 1
            elif direction == "N":
                i -= 1
            elif direction == "S":
                i += 1
            else:
                raise RuntimeError(f"Invalid direction: {direction}")

            if i >= 0 and j >= 0 and i < len(self.x) and j < len(self.y):
                entry = T[i, j]
            else:
                output = False
                break

            if entry == TRACK_NW and direction == "E":
                direction = "N"
            elif entry == TRACK_NW and direction == "S":
                direction = "W"
            elif entry == TRACK_SE and direction == "W":
                direction = "S"
            elif entry == TRACK_SE and direction == "N":
                direction = "E"
            elif entry == TRACK_SW and direction == "E":
                direction = "S"
            elif entry == TRACK_SW and direction == "N":
                direction = "W"
            elif entry == TRACK_NE and direction == "S":
                direction = "E"
            elif entry == TRACK_NE and direction == "W":
                direction = "N"
            elif (
                (entry == "-" and direction in ("E", "W")) or
                (entry == "|" and direction in ("N", "S"))
            ):
                pass
            elif entry == "":  # path incomplete
                break
            else:
                output = False

            path.add((i, j))

        if (i, j) == self.end and output:  # check for full path
            for (a, b) in itertools.product(
                    range(len(self.x)), range(len(self.y))
                    ):
                if (a, b) not in path and T[a, b] not in (".", ""):
                    output = False
                    break

        return output

    def _is_valid(self, T):
        if (((T != ".") & (T != "")).sum(axis=0) > self.x).any():
            output = False
        elif ((T != ".").sum(axis=0) < self.x).any():
            output = False
        elif (((T != ".") & (T != "")).sum(axis=1) > self.y).any():
            output = False
        elif ((T != ".").sum(axis=1) < self.y).any():
            output = False
        else:
            output = self._is_path(T)
        return output

    def solve(self, verbose=True):
        i = 0
        T = self.track.copy()
        possible_entries = self._possible_entries
        if verbose:
            pbar = tqdm()
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
                i -= 1
                T = possible_entries[i][1].copy()
            if verbose:
                pbar.update(1)

        solution = possible_entries[self._count - 1][1]
        self.solution = solution

        if verbose:
            for row in solution:
                print("".join(row))

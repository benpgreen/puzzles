import numpy as np

from tqdm import tqdm


TRACK_SE = "\u256d"
TRACK_SW = "\u256e"
TRACK_NW = "\u256f"
TRACK_NE = "\u2570"


test = {
    "tracks": [(5, 0, "-"), (2, 4, TRACK_SE), (5, 5, "|")],
    "x": [3, 6, 5, 1, 3, 6],
    "y": [5, 3, 4, 4, 4, 4]
}

test2 = {
    "tracks": [(0, 0, TRACK_SW), (4, 3, "-"), (5, 0, "|")],
    "x": [5, 2, 3, 3, 4, 3],
    "y": [1, 1, 5, 4, 6, 3]
}

test3 = {
    "tracks": [(4, 0, TRACK_SW), (4, 3, TRACK_NE), (5, 4, "|")],
    "x": [2, 3, 3, 4, 6, 2],
    "y": [2, 3, 3, 5, 4, 3]
}

test200 = {
    "tracks": [(6, 0, TRACK_NW), (9, 0, "|"), (3, 9, TRACK_NW)],
    "x": [7, 8, 3, 4, 7, 4, 3, 4, 2, 2],
    "y": [7, 6, 6, 4, 5, 3, 5, 6, 1, 1]
}

test31 = {
    "tracks": [(4, 0, TRACK_SW), (7, 7, "|")],
    "x": [2, 1, 2, 5, 3, 1, 7, 8],
    "y": [4, 4, 5, 3, 5, 5, 2, 1]
}


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
        self.track_locations = set()
        for i, j, entry in track_locations:
            self.track[i, j] = entry
            self.track_locations.add((i, j))
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
        if self.x.sum() != self.y.sum():
            raise ValueError(f"Invalid x and y args, must sum to same total")
        self._count = self.x.sum()

    def _is_valid(self, T):
        if ((T != "").sum(axis=0) > self.x).any():
            output = False
        elif ((T != "").sum(axis=1) > self.y).any():
            output = False
        else:
            output = True
        return output

    def _adjust_position(self, i, j, entry, direction, check=False):
        if direction == "E" and entry == "-":
            j += 1
        elif direction == "E" and entry == TRACK_NW:
            i -= 1
            direction = "N"
        elif direction == "E" and entry == TRACK_SW:
            i += 1
            direction = "S"
        elif direction == "W" and entry == "-":
            j -= 1
        elif direction == "W" and entry == TRACK_NE:
            i -= 1
            direction = "N"
        elif direction == "W" and entry == TRACK_SE:
            i += 1
            direction = "S"
        elif direction == "N" and entry == "|":
            i -= 1
        elif direction == "N" and entry == TRACK_SE:
            j += 1
            direction = "E"
        elif direction == "N" and entry == TRACK_SW:
            j -= 1
            direction = "W"
        elif direction == "S" and entry == "|":
            i += 1
        elif direction == "S" and entry == TRACK_NE:
            j += 1
            direction = "E"
        elif direction == "S" and entry == TRACK_NW:
            j -= 1
            direction = "W"
        elif check:
            direction = None
        else:
            raise RuntimeError(
                f"Invalid i, j, entry, direction: {i, j, entry, direction}"
            )
        return i, j, direction

    def solve(self, verbose=False):
        count = 0
        i, j, direction = self.start
        T = self.track.copy()
        self._possible_entries = {}
        self._count_to_pos = {}
        new_layer = True
        if verbose:
            pbar = tqdm()

        while count < self._count:

            if i < 0 or j < 0 or i >= len(self.x) or j >= len(self.y):
                # gone out of bounds, send back
                count -= 1
                self._possible_entries[count][0] += 1
                new_layer = False
                i, j, direction = self._count_to_pos[count]
                T = self._possible_entries[count][2].copy()
            else:

                if new_layer:
                    # gone into a new layer, so need to initialise it
                    if (i, j) in self.track_locations:
                        options = [T[i, j]]
                        d = self._adjust_position(
                            i, j, options[0], direction, check=True
                        )[-1]
                        if d is None:
                            T[i, j] = ""
                            count -= 1
                            self._possible_entries[count][0] += 1
                            new_layer = False
                            i, j, direction = self._count_to_pos[count]
                            T = self._possible_entries[count][2].copy()
                            continue
                    elif T[i, j] != "":
                        T[i, j] = ""
                        count -= 1
                        self._possible_entries[count][0] += 1
                        new_layer = False
                        i, j, direction = self._count_to_pos[count]
                        T = self._possible_entries[count][2].copy()
                        continue
                    elif direction == "E":
                        options = ["-", TRACK_NW, TRACK_SW]
                    elif direction == "W":
                        options = ["-", TRACK_NE, TRACK_SE]
                    elif direction == "N":
                        options = ["|", TRACK_SW, TRACK_SE]
                    elif direction == "S":
                        options = ["|", TRACK_NW, TRACK_NE]
                    else:
                        raise RuntimeError("WTF!")

                    entry = options[0]
                    T[i, j] = entry
                    if self._is_valid(T):  # then log this
                        self._possible_entries[count] = [0, options, T.copy()]
                        self._count_to_pos[count] = i, j, direction
                        i, j, direction = self._adjust_position(
                            i, j, entry, direction
                        )
                        count += 1
                        new_layer = True
                    else:
                        T[i, j] = ""
                        count -= 1
                        self._possible_entries[count][0] += 1
                        new_layer = False
                        i, j, direction = self._count_to_pos[count]
                        T = self._possible_entries[count][2].copy()
                else:
                    idx = self._possible_entries[count][0]
                    if idx < len(self._possible_entries[count][1]):
                        entry = self._possible_entries[count][1][idx]
                        T[i, j] = entry
                        self._possible_entries[count][2] = T.copy()
                        i, j, direction = self._adjust_position(
                            i, j, entry, direction
                        )
                        count += 1
                        new_layer = True
                    else:
                        count -= 1
                        self._possible_entries[count][0] += 1
                        new_layer = False
                        i, j, direction = self._count_to_pos[count]
                        T = self._possible_entries[count][2].copy()

            if verbose:
                pbar.update(1)

        solution = self._possible_entries[self._count - 1][2]
        self._count_to_pos = self._count_to_pos
        self._possible_entries = self._possible_entries
        self.solution = solution
        self.viz()

    def viz(self):
        print(" ".join([str(n) for n in self.x]))
        for idx, row in enumerate(self.solution):
            r = row.copy()
            r[r == ""] = "."
            print(" ".join(r) + f" {self.y[idx]}")

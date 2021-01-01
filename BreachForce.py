"""
Program to brute force a breach path for the breach minigame in Cyberpunk 2077
CodeMatrix: Represents the code matrix, a 5 by 5 grid of values.  Selecting values from the code matrix must follow
    certain rules:  Rule 1) Must select from first row first
                    Rule 2) Each subsequent selection must be perpendicular to the last selection
    Generates sequences when given a sequence length, of all possible sequences (Yes, this is a large number)

Sequence: Represents a result from the code matrix, including the coordinates (0 indexed) or a sequence for an upload
        (which will have 0,0 for each of it's positions.
        contains operator will work between two sequences and returns true if sequence A is inside sequence B
"""


class CodeMatrix:
    def __init__(self, matrix):
        assert isinstance(matrix, list)
        # assert len(matrix) == 5
        for row in matrix:
            assert len(row) == len(matrix)
        self.matrix = matrix
        self.recursions = 0

    def permutations(self, length, path=[]):
        """
        Generates all possible permutations from the matrix of the given length.
        :param length:  How many more characters to add,
        :param path:  The path so far. If a coord is in the path, it's considered "used"
        :return: Yields a sequence
        """
        self.recursions += 1
        assert length < 12
        if length <= 0:
            # We have a full path, let's generate a sequence and yield it.
            # We first need the actual values
            yield Sequence([self.matrix[row][col] for row, col in path], path)
        else:
            # First, figure out which row/col we're on, and what direction we're going.
            # axis represents if we have to select from a ROW or COL.  if axis == 0, select along row axis
            # else, select along col axis (that is, loop through to select each item from that row or col)
            axis = len(path) % 2
            # Last is the last row or last col that was selected from.
            if len(path) > 0:
                last = path[-1][axis]
            else:
                last = 0
            # Now, for each element in the row/col perpendicular to the last selection, put it in a copy of the path
            # and recursively call
            for i in range(len(self.matrix)):
                if axis == 0:
                    next = (last, i)
                else:
                    next = (i, last)
                if next not in path:
                    new_path = path + [next]

                    yield from self.permutations(length - 1, new_path)


class Sequence:
    def __init__(self, values, path=[]):
        """
        :param values: The codes for this sequence
        :param path: When generating a path, this is a list of (row, column) tuples that correspond to each value
        """
        self.values = values
        self.path = path

    def __contains__(self, item):
        assert isinstance(item, Sequence)
        """Returns true if item is a subsequence of self"""
        other_seq = " ".join(item.values)
        my_seq = " ".join(self.values)
        return other_seq in my_seq


    def __len__(self):
        return len(self.path)

    def __repr__(self):
        out = []
        for i, item in enumerate(self.values):
            v = f"({item})"
            if i < len(self.path):
                v += str(self.path[i])
            out.append(v)
        return "->".join(out)

    def __str__(self):
        return self.__repr__()

    def get_coords(self):
        return self.path


def solve(matrix, buffers, *targets):
    for path in matrix.permutations(buffers):
        if all([t in path for t in targets]):
            return path
    return None


if __name__ == "__main__":
    """Testing"""
    a = Sequence(['1C', '1C', '55', 'BD', '1C'])
    b = Sequence(['1C', '55', 'BD'])
    c = Sequence(['1C', '55', '1C'])
    print("Sequence A:", a)
    print("Sequence B:", b)
    print("Sequence C:", c)
    print("Is b in a?:", b in a)
    print("is c in a?:", c in a)
    codeList = [['55', '1C', '55', '1C', 'BD'],
                ['1C', '55', '1C', 'E9', '1C'],
                ['1C', 'BD', '1C', '55', '55'],
                ['BD', '55', '55', '55', '55'],
                ['BD', '1C', '55', 'BD', '1C']]
    code = CodeMatrix(codeList)
    for path in code.permutations(7):
        # print("A path:", path)
        if b in path and c in path:
            print("<--- Found Path! --->")
            print(path)
            break
    print("Path Found:", solve(code, 7, b, c))
    #
    # hardCode = [['55', '7A', '55', 'BD', 'E9', '1C'],
    #             ['7A', '7A', '55', '1C', '1C', '1C'],
    #             ['55', '55', '55', 'BD', '55', 'BD'],
    #             ['7A', '1C', '55', '1C', '7A', 'E9'],
    #             ['1C', 'BD', '55', 'E9', '7A', 'E9'],
    #             ['E9', 'E9', '55', 'BD', 'BD', '1C']]
    # hardMatrix = CodeMatrix(hardCode)
    # v1 = Sequence(['1C', '1C'])
    # v2 = Sequence(['E9', '55', '1C'])
    # v3 = Sequence(['E9', '7A', 'BD', 'E9'])
    #
    # print("Trying hard matrix")
    # for path in hardMatrix.permutations(7):
    #     if v1 in path and v2 in path and v3 in path:
    #         print("Path Found for ALL:", path)
    #     elif v1 in path and v2 in path:
    #         print("Path Found for v12:", path)
    #     elif v1 in path and v3 in path:
    #         print("Path Found for v13:", path)
    #     elif v2 in path and v3 in path:
    #         print("Path Found for v23:", path)
    # print("Tried", hardMatrix.recursions, "different paths")
    # print("Finished")

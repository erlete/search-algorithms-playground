"""Main generator and solver module for search algorithms testing."""

from random import randint, sample
from time import time


class Maze:
    """This class generates a blank array of (m x n) dimensions, made of '0'
    values, stored in the 'Base' attribute.

    Given that array, an algorithm generates a 'path', made out of '1' values,
    which later on can be evaluated by a search algorithm in order to explore
    the path. Explored nodes have a numerical value of '2'.

    The initial and goal states are represented by '-10' and '10' values,
    respectively.
    """
    def __init__(self, dimensions=10):
        if isinstance(dimensions, int) and dimensions > 1:
            self.Dimensions = (dimensions, dimensions)
        elif (isinstance(dimensions, tuple) and len(dimensions) == 2
                and dimensions[0] > 1 and dimensions[1] > 1):
            self.Dimensions = (dimensions[0], dimensions[1])
        else:
            raise Exception(
                "Dimensions must be either an 'int' or a 2-tuple of 'int's \
                greater than '1'."
                )

        self.Base = [
            [0 for col in range(self.Dimensions[1])]
            for row in range(self.Dimensions[0])
            ]

        self.Base[0][0] = -10  # Initial state.
        self.Initial = (0, 0)  # Initial position.
        self.Goal = (0, 0)  # Final position

        self.Distances = {}  # Distances tracking for solving methods.

    def nextnodes(self, coordinates):
        """Gets the nodes immediately next to the given coordinates from
        'self.Base'.

        The order in which the surrounding nodes are returned is set in a
        random way, in order to prevent data pre-setting.

        Process illustration:
        ---------------------

                T
            L   X   R
                B
        """
        nodes = [
            (coordinates[0] - 1, coordinates[1]),   # Top
            (coordinates[0], coordinates[1] + 1),   # Right
            (coordinates[0] + 1, coordinates[1]),   # Bottom
            (coordinates[0], coordinates[1] - 1)    # Left
            ]
        nextNodes = [
            node for node in nodes
            if 0 <= node[0] <= self.Dimensions[0] - 1
            and 0 <= node[1] <= self.Dimensions[1] - 1
            ]
        return sample(nextNodes, len(nextNodes))

    def surroundings(self, coordinates):
        """Gets the values in the square surroundings of the given coordinates.
        This method is used in order to prevent path mixing during generation.

        Since the method is only used to evaluate the amount of nearby 'path'
        values near the considered node during path generation, there is no
        point in returning a randomized sample.

        Process illustration:
        ---------------------

            TL  TC  TR
            ML  XX  MR
            BL  BC  BR
        """
        nodes = [
            (coordinates[0] - 1, coordinates[1] - 1),   # Top left
            (coordinates[0] - 1, coordinates[1]),       # Top center
            (coordinates[0] - 1, coordinates[1] + 1),   # Top right
            (coordinates[0], coordinates[1] + 1),       # Middle right
            (coordinates[0] + 1, coordinates[1] + 1),   # Bottom right
            (coordinates[0] + 1, coordinates[1]),       # Bottom center
            (coordinates[0] + 1, coordinates[1] - 1),   # Bottom left
            (coordinates[0], coordinates[1] - 1)        # Middle left
            ]
        return [
            node for node in nodes
            if 0 <= node[0] <= self.Dimensions[0] - 1
            and 0 <= node[1] <= self.Dimensions[1] - 1
            ]

    def caesar(self, nodes):
        """Random path divergence generator. Takes one or multiple path
        divergence possibilities and selects at least one of them.

        The name is due to the 'lives, dies' choice of Julius Caesar during
        colosseum gladiator games.
        """
        return sample(nodes, randint(1, len(nodes))) if len(nodes) > 0 else []

    def goalspreader(self, path_tiles):
        """Sets the position of the goal state at the farthest possible
        coordinate in the array.
        """
        distance = (
            self.Initial[0] + path_tiles[0][0],
            self.Initial[1] + path_tiles[0][1]
            )
        for path in path_tiles:
            if ((self.Initial[0] + path[0], self.Initial[1] + path[1])
                    >= distance):
                distance = (self.Initial[0] + path[0],
                            self.Initial[1] + path[1])
        return (distance[0] - self.Initial[0], distance[1] - self.Initial[1])

    def pathgenerator(self):
        """Randomly generates a pathway for the array."""
        ts = time()
        print(' Generating array... '.center(self.Dimensions[1] * 2 + 2, '-'))

        frontier = [self.Initial]

        while True:
            selectedNodes, candidates = [], []

            for node in frontier:
                candidates.extend(
                    [neighbor for neighbor in self.nextnodes(node)
                        if self.Base[neighbor[0]][neighbor[1]] not in [-10, 1]]
                    )
            candidates = list(set(candidates))

            for candidate in candidates:
                nearbyPathTiles = len(
                    [node for node in self.surroundings(candidate)
                        if self.Base[node[0]][node[1]] in [1, -10]]
                    )
                avaliablePath = True if nearbyPathTiles < 3 else False
                selectedNodes.append(candidate) if avaliablePath else None

            selectedNodes = self.caesar(selectedNodes)

            if selectedNodes == []:
                self.Goal = self.goalspreader(frontier)
                self.Base[self.Goal[0]][self.Goal[1]] = 10

                te = time()
                print(
                    f' Array generated correctly. Time elapsed: \
                    {(te - ts):.4}s. '.center(self.Dimensions[1] * 2 + 2, '-')
                    )

                return None

            frontier.extend(selectedNodes)
            for coordinates in selectedNodes:
                self.Base[coordinates[0]][coordinates[1]] = 1

        self.Distances = dict()
        for row in range(len(self.Base)):
            for column in range(len(self.Base[row])):
                if self.Base[row][column] == 1:
                    self.Distances[(row, column)] \
                        = self.manhattan((row, column))

    def manhattan(self, coordinates: tuple):
        """Returns the manhattan distance between two nodes (sum of the
        absolute cartesian coordinates difference between a selected node and
        the goal node).The values are set as absolute to prevent search
        deviations due to negative coordinates addition.
        """
        return abs(self.Goal[0] - coordinates[0]) \
            + abs(self.Goal[1] - coordinates[1])

    def dfs(self):
        """Depth-First Search (DFS)."""
        self.Distances = dict()
        for row in range(len(self.Base)):
            for column in range(len(self.Base[row])):
                if self.Base[row][column] == 1:
                    self.Distances[(row, column)] \
                        = self.manhattan((row, column))

        ts = time()
        print(' Searching array... '.center(self.Dimensions[1] * 2 + 2, '-'))
        explored = list()
        frontier = self.nextnodes(self.Initial)

        while True:

            if len(frontier) >= 1:
                node = frontier[-1]
                frontier = frontier[:-1]

                if node not in [self.Initial, self.Goal]:
                    self.Base[node[0]][node[1]] = 2
                    explored.append(node) if node not in explored else None

                    for neighbor in self.nextnodes(node):
                        if self.Base[neighbor[0]][neighbor[1]] == 1:
                            frontier.append(neighbor) \
                                if neighbor not in frontier else None
                        elif self.Base[neighbor[0]][neighbor[1]] == 10:
                            te = time()
                            print(
                                f' Array searched correctly. Time elapsed: \
                                {(te - ts):.4}s. '.center(
                                    self.Dimensions[1] * 2 + 2, '-'
                                    )
                                )
                            return 1

            else:
                return 0

    def gbfs(self):
        """Greedy Best-First Search (GBFS)."""
        self.Distances = dict()
        for row in range(len(self.Base)):
            for column in range(len(self.Base[row])):
                if self.Base[row][column] == 1:
                    self.Distances[(row, column)] \
                         = self.manhattan((row, column))
        ts = time()
        print(' Searching array... '.center(self.Dimensions[1] * 2 + 2, '-'))
        frontier, explored = list(), [self.Initial]
        for node in self.nextnodes(self.Initial):
            if self.Base[node[0]][node[1]] == 1:
                frontier.append(node)

        while True:

            if len(frontier) >= 1:

                node = frontier[-1]
                for candidate in frontier:
                    if (self.Distances[(candidate[0], candidate[1])]
                            < self.Distances[(node[0], node[1])]):
                        node = candidate
                del frontier[frontier.index(node)]

                if node not in [self.Initial, self.Goal]:
                    self.Base[node[0]][node[1]] = 2
                    explored.append(node) if node not in explored else None

                    for neighbor in self.nextnodes(node):
                        if self.Base[neighbor[0]][neighbor[1]] == 1:
                            frontier.append(neighbor) \
                                if neighbor not in frontier else None
                        elif self.Base[neighbor[0]][neighbor[1]] == 10:
                            te = time()
                            print(
                                f' Array searched correctly. Time elapsed: \
                                {(te - ts):.4}s. '.center(
                                    self.Dimensions[1] * 2 + 2, '-'
                                    )
                                )
                            return 1

            else:
                return 0

    def __repr__(self):
        visual = {0: '█ ', 1: '  ', 2: '░ ',
                  3: '≡ ', -10: 'A ', 10: 'B '}
        return (
            f"╔═{2 * '═' * self.Dimensions[1]}╗\n"
            + ''.join(
                ''.join(
                    ['║ ' + ''.join(
                        [visual[element] for element in row]
                    ) + '║\n']
                ) for row in self.Base
            ) + f"╚═{2 * '═' * self.Dimensions[1]}╝"
            )

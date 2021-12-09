"""Main generator and solver module for search algorithms testing."""


from PIL import Image, ImageDraw
from math import log
from random import randint, randrange, sample
from time import time
from datetime import datetime


class Unnamed:
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary


    def __eq__(self, element):
        if isinstance(element, Unnamed):
            return True if self.primary == element.primary else False
        raise Exception(f"Can't compare <class 'Unnamed'> with {type(element)}.")

    def __gt__(self, element):
        if isinstance(element, Unnamed):
            return True if self.primary > element.primary else False
        raise Exception(f"Can't compare <class 'Unnamed'> with {type(element)}.")

    def __lt__(self, element):
        if isinstance(element, Unnamed):
            return True if self.primary < element.primary else False
        raise Exception(f"Can't compare <class 'Unnamed'> with {type(element)}.")

    def __repr__(self):
        return f"(P: {self.primary}, S: {self.secondary})"


class Node:
    def __init__(self, x: int, y: int, state = 0):
        self.X = x
        self.Y = y
        self.coordinates = (self.X, self.Y)
        self.state = state

    def __eq__(self, element):
        if isinstance(element, Node):
            return True if self.X + self.Y == element.X + element.Y else False
        raise Exception(f"Can't compare <class 'Node'> with {type(element)}.")

    def __gt__(self, element):
        if isinstance(element, Node):
            return True if self.X + self.Y > element.X + element.Y else False
        raise Exception(f"Can't compare <class 'Node'> with {type(element)}.")

    def __lt__(self, element):
        if isinstance(element, Node):
            return True if self.X + self.Y < element.X + element.Y else False
        raise Exception(f"Can't compare <class 'Node'> with {type(element)}.")

    def __repr__(self):
        return f"(X: {self.X}, Y: {self.Y}, S: {self.state})"


class Maze:
    """This class generates a blank array of (m x n) dimensions, made of '0'
    values, stored in the 'Base' attribute.

    Given that array, an algorithm generates a 'path', made out of '1' values,
    which later on can be evaluated by a search algorithm in order to explore
    the path. Explored nodes have a numerical value of '2'.

    The initial and goal states are represented by '-10' and '10' values,
    respectively.
    """

    def __init__(self, dimensions = (10, 10), verbose = False):
        if isinstance(dimensions, tuple):
            if  (dimensions[0] + dimensions[1]) / 2 > 1:
                self.DIMENSIONS = dimensions
                self.X = self.DIMENSIONS[0]
                self.Y = self.DIMENSIONS[1]
            else:
                raise Exception("Tuple's elements must be integers greater "
                                "than one.")
        else:
            raise Exception("Dimensions must be a 2-tuple")

        self.base = [
            [Node(column, row, 0) for column in range(self.X)]
            for row in range(self.Y)
        ]

        self.node_map = []
        for row in self.base:
            self.node_map.extend(row)

        self.verbose = verbose

        self.start = self.base[randrange(0, self.Y)][randrange(0, self.X)]
        self.start.state = -10

        self.log(f"Start: {self.start}")

        self.distances = {}

        self.log(["Node map:"] + [row for row in self.base])


    def log(self, argument, hierarchy = 0, plain = False):
        """Visual log implementation for debugging."""

        if self.verbose:
            if plain:
                print(argument)

            else:
                if isinstance(argument, str):
                    title = f"{datetime.now().isoformat()} -> {argument}"
                    print(title.rjust(len(title) + 1 + 4 * hierarchy, '-'))

                elif isinstance(argument, list):
                    title = f"{datetime.now().isoformat()} -> {argument[0]}"
                    print(title.rjust(len(title) + 1 + 4 * hierarchy, '-'))

                    for element in argument[1:]:
                        subtitle = f"{element}"
                        print(subtitle.rjust(len(subtitle) + 1 + 4 * (hierarchy + 1), '-'))

            print()


    def next_nodes(self, node: Node, hierarchy = 1) -> list:
        """Gets the nodes immediately next to the given coordinates from
        'self.base'.

        The order in which the surrounding nodes are returned is set in a
        random way, in order to prevent data pre-setting.

        Process illustration:
        ---------------------

                T
            L   X   R
                B
        """

        coordinates = (
            (node.X, node.Y - 1),  # Top
            (node.X + 1, node.Y),  # Right
            (node.X, node.Y + 1),  # Bottom
            (node.X - 1, node.Y)   # Left
        )

        self.log([f"[NEXT_NODES] (Node: {node}) Coordinates:", coordinates], hierarchy=hierarchy)

        nodes = [
            self.base[coord[1]][coord[0]] for coord in coordinates
            if 0 <= coord[0] < self.X and 0 <= coord[1] < self.Y
        ]

        self.log([f"[NEXT_NODES] (Node: {node}) Nodes:", nodes], hierarchy=hierarchy + 1)

        return sample(nodes, len(nodes))


    def surrounding_nodes(self, node: Node, hierarchy = 1) -> list:
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

        coordinates = (
            (node.X - 1, node.Y - 1),  # Top left
            (node.X, node.Y - 1),      # Top center
            (node.X + 1, node.Y - 1),  # Top right
            (node.X + 1, node.Y),      # Middle right
            (node.X + 1, node.Y + 1),  # Bottom right
            (node.X, node.Y + 1),      # Bottom center
            (node.X - 1, node.Y + 1),  # Bottom left
            (node.X - 1, node.Y)       # Middle left
        )

        self.log([f"[SURROUNDING_NODES] (Node: {node}) Coordinates:", coordinates], hierarchy=hierarchy)

        nodes = [
            self.base[coord[1]][coord[0]] for coord in coordinates
            if 0 <= coord[0] < self.X and 0 <= coord[1] < self.Y
        ]

        self.log([f"[SURROUNDING_NODES] (Node: {node}) Nodes:", nodes], hierarchy=hierarchy + 1)

        return nodes


    def caesar(self, nodes, bias=0):
        """Random path divergence generator. Takes one or multiple path
        divergence possibilities and selects at least one of them.

        The name is due to the 'lives, dies' choice of Julius Caesar during
        colosseum gladiator games.
        """

        chance = randint(bias if bias <= len(nodes) else len(nodes), len(nodes))
        return sample(nodes, chance if 0 <= chance <= len(nodes) else 0)


    def goal_spreader(self) -> None:
        """Sets the position of the goal state at the farthest possible
        coordinate in the array.
        """

        path_tiles = [node for node in self.node_map if node.state == 1]

        self.log(["[GOAL_SPREADER] Elements:", path_tiles], hierarchy=2)

        self.end = path_tiles[0]
        top_distance = self.manhattan(self.end, path_tiles[0])

        for tile in path_tiles:
            if self.manhattan(self.start, tile) > top_distance:
                top_distance = self.manhattan(self.start, tile)
                self.end = tile

        self.end.state = 10

        self.log(["[GOAL_SPREADER] Selected goal:", self.end], hierarchy=3)


    def path_generator(self, bias=5):
        """Randomly generates a pathway for the array."""

        timer_start = time()
        frontier = [self.start]

        self.log(["[PATH_GENERATOR] Frontier:", frontier])

        while frontier != []:
            self.log("[PATH_GENERATOR] Beginning iteration:")

            selected_nodes, candidates = [], []

            for index, node in enumerate(frontier):
                candidates.extend(
                    [neighbor for neighbor in self.next_nodes(node, hierarchy=1)
                    if neighbor.state not in (-10, 1)]
                )

            self.log(["[PATH_GENERATOR] Candidates:", candidates], hierarchy=1)

            selected_nodes = [
                candidate for candidate in candidates if len([
                    node for node in self.surrounding_nodes(candidate)
                    if self.base[node.Y][node.X].state in (-10, 1)
                ]) < 3
            ]

            self.log(["[PATH_GENERATOR] Selected nodes (pre-caesar):", selected_nodes], hierarchy=1)

            selected_nodes = self.caesar(selected_nodes, bias=int(log(self.X ** self.Y) ** (1 / bias)))

            self.log(["[PATH_GENERATOR] Selected nodes (post-caesar):", selected_nodes], hierarchy=1)

            frontier = selected_nodes
            for node in frontier:
                node.state = 1

            self.log(["[PATH_GENERATOR] Frontier:", frontier], hierarchy=1)

            self.log(self, plain=True)

        self.goal_spreader()

        timer_end = time()

        print(f"Array generated correctly. Time elapsed: {(timer_end - timer_start):.4f} seconds.")

        self.log(self, plain=True)


    @staticmethod
    def manhattan(node_1: Node, node_2: Node):
        """Returns the manhattan distance between two nodes (sum of the
        absolute cartesian coordinates difference between a selected node and
        the goal node).
        """

        return abs(node_1.X - node_2.X) + abs(node_1.Y - node_2.Y)


    def dfs(self):
        """Depth-First Search (DFS)."""

        # self.distances = dict()
        # for row in range(self.Y):
        #     for column in range(self.X):
        #         if self.base[row][column] == 1:
        #             self.distances[(row, column)] = self.manhattan((row, column))

        self.distances = {
            node.coordinates: self.manhattan(node, self.end) for node in self.node_map
            if node.state == 1
        }

        timer_start = time()

        frontier, explored = self.next_nodes(self.start), []

        while len(frontier) >= 1:
            node = frontier.pop()

            if node.state not in (-10, 10):
                node.state = 2
                explored.append(node)# if node not in explored else None # TODO: remove this?

                for neighbor in self.next_nodes(node):
                    if neighbor.state == 1:
                        frontier.append(neighbor)# if neighbor not in frontier else None # TODO: remove this?

                    elif neighbor.state == 10:
                        timer_end = time()
                        print(f"Array searched correctly. Time elapsed: {(timer_end - timer_start):.4}s.")

                        return True, explored
        return False, explored


    def gbfs(self):
        """Greedy Best-First Search (GBFS)."""

        self.distances = {
            node.coordinates: self.manhattan(node, self.end) for node in self.node_map
            if node.state == 1
        }

        timer_start = time()

        frontier, explored = [Unnamed(0, self.start)], []

        while len(frontier) >= 1:

            self.log("[GBFS] Beginning iteration:")

            self.log(["[GBFS] Frontier:", frontier])

            node = frontier.pop().secondary
            node.state = 2 if node.state != -10 else -10
            explored.append(node)

            self.log(["[GBFS] Selected node:", node])

            self.log(self, plain=True)

            candidates = [node for node in self.next_nodes(node) if node.state in (1, 10)]

            if any(candidate.coordinates == self.end.coordinates for candidate in candidates):
                self.log(["[GBFS] End node:", self.end])
                timer_end = time()
                print(f"Array searched correctly. Time elapsed: {(timer_end - timer_start):.6f} seconds.")
                return True, explored

            self.log(["[GBFS] Candidates:", candidates], hierarchy=1)

            weights = [Unnamed(self.distances[candidate.coordinates], candidate) for candidate in candidates]

            self.log(["[GBFS] Weight list:", weights], hierarchy=1)

            frontier.extend(weights)
            frontier = sorted(frontier, reverse=True)

        self.log(["[GBFS] End node:", self.end])

        return False, explored


    def __repr__(self):
        visual = {0: '█ ', 1: '  ', 2: '░ ',
                  3: '≡ ', -10: 'A ', 10: 'B '}

        return (
            f"╔═{2 * '═' * self.X}╗\n"
            + ''.join(
                ''.join(
                    ['║ ' + ''.join(
                        [visual[element.state] for element in row]
                    ) + '║\n']
                ) for row in self.base
            ) + f"╚═{2 * '═' * self.X}╝"
            )


    def display(self):

        # Dimensions:
        cell = 50
        border = 2

        # Canvas:
        img = Image.new(
            mode="RGBA",
            size=(self.DIMENSIONS[1] * cell, self.DIMENSIONS[0] * cell),
            color="black"
        )

        draw = ImageDraw.Draw(img)

        for i, row in enumerate(self.base):
            for j, column in enumerate(row):

                # Walls
                if column.state == 0:
                    fill = (40, 40, 40)

                # Start
                elif column.state == -10:
                    fill = (255, 0, 0)

                # Goal
                elif column.state == 10:
                    fill = (50, 171, 28)

                # Explored
                elif column.state == 2:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell + border, i * cell + border),
                      ((j + 1) * cell - border, (i + 1) * cell - border)]),
                    fill=fill
                )

        img.show()


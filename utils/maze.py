"""Container module for the maze classes.

This module contains two classes: one of them is a generic Maze interface that
contains basic attributes and methods, while the other is a specific maze
implementation that uses a 2D array as a data structure and contains methods
that allow path generation and searching.

Author:
-------
 - Paulo Sánchez (@erlete)
"""


from datetime import datetime
from os import mkdir, path
from random import randint, randrange, sample
from time import time

from PIL import Image, ImageDraw

from utils.frontier import QueueFrontier, StackFrontier
from utils.node import Node


class MazeBase:
    """Contains basic methods and attributes related to maze generation.

    This class defines several properties such as width, height, start and end
    nodes for the maze generation process.

    Parameters:
    -----------
     - dimensions: int, tuple
        The dimensions of the maze. If an integer is passed, the maze will be
        square. If a tuple is passed, the first element will be the width and
        the second element will be the height.
     - logger: bool
        If True, the class will print information about the maze generation
    """

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        if isinstance(value, tuple):
            if len(value) != 2 or not all(isinstance(dimension, int) for dimension in value):
                raise TypeError("'dimensions' must be a tuple of 2 integers.")
            elif value[0] <= 3 or value[1] <= 3:
                raise ValueError(
                    "each 'dimensions' value must be greater than 3.")

            self._dimensions = value

        elif isinstance(value, int):
            if value <= 3:
                raise ValueError("'dimensions' must be greater than 3.")

            self._dimensions = (value, value)

        else:
            raise TypeError(
                "'dimensions' must be an integer or a tuple of them.")

        self._width, self._height = self._dimensions  # Unpacks the tuple.

    def __init__(self, dimensions, logger=False):
        self.dimensions = dimensions

        # Maze generation process:
        self._node_matrix = [
            [Node(column, row) for column in range(self._width)]
            for row in range(self._height)
        ]

        self._node_list = [node for row in self._node_matrix for node in row]

        self._start = self._node_matrix[
            randrange(0, self._height)
        ][randrange(0, self._width)]
        self._start.set_state(-10)
        self._end = Node(0, 0)

        # Maze statistics initialization:
        self._explored_nodes, self.optimal_path = [], []
        self._is_generated = self._is_explored = False
        self._count = {
            "path": 0,
            "explored": 0,
            "total": self._width * self._height
        }


class Search:
    """Contains search algorithms and methods related to maze exploration."""

    @staticmethod
    def manhattan_distance(start: Node, end: Node) -> int:
        """Returns the manhattan_distance distance between two nodes (sum of
        the absolute cartesian coordinates difference between two nodes).

        Parameters:
        -----------
         - start : Node
            The starting node.
         - end : Node
            The ending node.
        """

        return abs(start.x - end.x) + abs(start.y - end.y)

    @staticmethod
    def radial_distance(start: Node, end: Node) -> float:
        """Returns the radial distance distance between two nodes (square root
        of the sum of each node's coordinates squared).

        Parameters
        ----------
         - start : Node
            The starting node.
         - end : Node
            The ending node.
        """

        return ((start.x - end.x) ** 2 + (start.y - end.y) ** 2) ** .5

    def depth_first_search(self) -> bool:
        """Depth-First Search method.

        Uses StackFrontier data structure, returning the last added node in
        the first place. This causes the algorithm to explore a path until
        it reaches a dead end, then backtracks to the last node that has
        unexplored neighbors and repeats the process.
        """

        if self._is_explored:
            self._reset_explored_nodes()

        timer = time()
        frontier = StackFrontier()
        frontier.add(self._start)
        self._is_explored, has_end = True, False

        self._log("[DFS] Initial frontier:", frontier)

        while not frontier.is_empty() and not has_end:
            self._explored_nodes.append(node := frontier.remove())
            if node.state != -10:
                node.set_state(2)

            self._log("[DFS] Selected node:", node)
            self._log(f"[DFS] Updated display:\n\n{self.ascii()}")

            neighbors = [
                node for node in self._get_neighbors(node)
                if node.state in (1, 10)
            ]

            for neighbor in neighbors:
                neighbor.set_parent(node)

                if neighbor.state == self._end.state:
                    self._explored_nodes.append(self._end)
                    has_end = True

                    self._log("[DFS] Search time:", f"{(time() - timer):.5}s.")
                    break

            frontier.add(neighbors)

            self._log("[DFS] Updated frontier:", frontier)

        self._count["explored"] = len(self._explored_nodes)
        self._set_node_color()
        self._get_optimal_path()
        return has_end

    def breadth_first_search(self) -> bool:
        """Breadth-First Search method.

        Uses QueueFrontier data structure, returning the first added node in
        the first place. This causes the algorithm to explore all possible
        paths simultaneously, taking more time to find the optimal path, but
        preventing dead-end search processes.
        """

        if self._is_explored:
            self._reset_explored_nodes()

        timer = time()
        frontier = QueueFrontier()
        frontier.add(self._start)
        self._is_explored, has_end = True, False

        self._log("[BFS] Initial frontier:", frontier)

        while not frontier.is_empty() and not has_end:
            self._explored_nodes.append(node := frontier.remove())
            if node.state != -10:
                node.set_state(2)

            self._log("[BFS] Selected node:", node)
            self._log(f"[BFS] Updated display:\n\n{self.ascii()}")

            neighbors = [
                node for node in self._get_neighbors(node)
                if node.state in (1, 10)
            ]

            for neighbor in neighbors:
                neighbor.set_parent(node)

                if neighbor.state == self._end.state:
                    self._explored_nodes.append(self._end)
                    has_end = True

                    self._log("[BFS] Search time:", f"{(time() - timer):.5}s.")
                    break

            frontier.add(neighbors)

            self._log("[BFS] Updated frontier:", frontier)

        self._count["explored"] = len(self._explored_nodes)
        self._set_node_color()
        self._get_optimal_path()
        return has_end

    def greedy_best_first_search(self) -> bool:
        """Greedy Best-First Search method.

        Uses the manhattan distance heuristic to find the path that is closest
        to the end, yet it doesn't guarantee the optimal path. This often
        causes the algorithm to search several dead-ends before finding the
        end node.
        """

        if self._is_explored:
            self._reset_explored_nodes()

        for node in self._node_list:
            node.weight = self.manhattan_distance(node, self._end)

        timer = time()
        frontier = [self._start]
        self._is_explored, has_end = True, False

        self._log("[GBFS] Initial frontier:", frontier)

        while len(frontier) >= 1 and not has_end:
            self._explored_nodes.append(node := frontier.pop())
            if node.state != -10:
                node.set_state(2)

            self._log("[GBFS] Selected node:", node)
            self._log(f"[GBFS] Updated display:\n\n{self.ascii()}")

            neighbors = [
                node for node in self._get_neighbors(node)
                if node.state in (1, 10)
            ]

            for neighbor in neighbors:
                neighbor.set_parent(node)

                if neighbor.state == self._end.state:
                    self._explored_nodes.append(self._end)
                    has_end = True

                    self._log("[GBFS] Search time:",
                              f"{(time() - timer):.5f}s.")
                    break

            self._log("[GBFS] Neighbors:", neighbors, indentation=1)

            frontier.extend(neighbors)
            frontier = sorted(frontier, reverse=True, key=lambda x: x.weight)

            self._log("[GBFS] Updated frontier:", frontier)

        self._count["explored"] = len(self._explored_nodes)
        self._set_node_color()
        self._get_optimal_path()
        return has_end

    def radial_search(self) -> bool:
        """Radial Search method.

        Uses the radial distance heuristic to find the path that is closest
        to the end, yet it doesn't guarantee the optimal path. This often
        causes the algorithm to search several dead-ends before finding the
        end node.
        """

        if self._is_explored:
            self._reset_explored_nodes()

        for node in self._node_list:
            node.weight = self.radial_distance(node, self._end)

        timer = time()
        frontier = [self._start]
        self._is_explored, has_end = True, False

        self._log("[RS] Initial frontier:", frontier)

        while len(frontier) >= 1 and not has_end:
            self._explored_nodes.append(node := frontier.pop())
            if node.state != -10:
                node.set_state(2)

            self._log("[RS] Selected node:", node)
            self._log(f"[RS] Updated display:\n\n{self.ascii()}")

            neighbors = [
                node for node in self._get_neighbors(node)
                if node.state in (1, 10)
            ]

            for neighbor in neighbors:
                neighbor.set_parent(node)

                if neighbor.state == self._end.state:
                    self._explored_nodes.append(self._end)
                    has_end = True

                    self._log("[RS] Search time:", f"{(time() - timer):.5f}s.")
                    break

            self._log("[RS] Neighbors:", neighbors, indentation=1)

            frontier.extend(neighbors)
            frontier = sorted(frontier, reverse=True, key=lambda x: x.weight)

            self._log("[RS] Updated frontier:", frontier)

        self._count["explored"] = len(self._explored_nodes)
        self._set_node_color()
        self._get_optimal_path()
        return has_end


class Maze(MazeBase, Search):
    """Represents a maze object.

    Contains methods for maze generation and exploration, as well as methods
    for exporting the maze to an image file and logging the process.

    Parameters:
    -----------
     - dimensions: int, tuple
        The dimensions of the maze. If an integer is passed, the maze will be
        square. If a tuple is passed, the first element will be the width and
        the second element will be the height.
     - logger: bool
        If True, the class will print information about the maze generation
    """

    def __init__(self, dimensions, logger=False):

        super().__init__(dimensions, logger)

        # Logger settings:
        self.logger = logger
        self.LOG_DIRECTORY = "log_cache"
        self.LOG_PREFIX = "log"
        self.LOG_FORMAT = "txt"
        self.LOG_FILE = f"./{self.LOG_DIRECTORY}/{self.LOG_PREFIX}_" +\
            f"{''.join(str(time()).split('.'))}.{self.LOG_FORMAT}"
        # Logs are dinamically modified, so its identifier must remain fixed
        #	so that more contents can be appended to them.

        # Image settings:
        self.IMAGE_DIRECTORY = "image_cache"
        self.IMAGE_PREFIX = "image"
        self.IMAGE_FORMAT = "png"
        self.IMAGE_FILE = None
        # Images might be exported several times per object creation, hence
        #	the necessity of making their identifier variable (in 'Maze.image').

        self._generate_path()

    @staticmethod
    def _writer(file: str, argument, indentation: int, newlines: int):
        """TODO: add docstring"""
        header = f"+ {datetime.now().isoformat()} "
        file.write(
            header.ljust(len(header) + 4 * (indentation + 1), '-')
            + f" {argument}" + newlines * '\n'
        )

    # TODO: refactor this method or remove it.
    def _log(self, *arguments, indentation=0, expand=True) -> None:
        """TODO: add docstring"""
        if not self.logger:
            return None

        if not path.isdir(f"./{self.LOG_DIRECTORY}"):
            mkdir(f"./{self.LOG_DIRECTORY}")

        with open(self.LOG_FILE, mode='a', encoding="utf-8") as log_file:
            if len(arguments) >= 1:
                self._writer(log_file, arguments[0], indentation, 1)

                if len(arguments) > 1:
                    for argument in arguments[1:]:
                        if isinstance(argument, (list, tuple, set)) and expand:
                            for index, element in enumerate(argument):
                                self._writer(
                                    log_file, f"{index} :: {element}", indentation + 2, 1)
                        else:
                            self._writer(log_file, argument,
                                         indentation + 1, 1)

            log_file.write('\n')

        return None

    def _set_node_color(self):
        """Automatically sets the color of all explored nodes.

        The color is set based on the count of currently explored nodes and
        the color difference between the endpoints."""

        # Set the color difference between each node:
        differential = (
            (self._end.color[0] - self._start.color[0]) /
            self._count["explored"],
            (self._end.color[1] - self._start.color[1]) /
            self._count["explored"],
            (self._end.color[2] - self._start.color[2]) /
            self._count["explored"],
        )

        # Apply the color to each explored node:
        for index, node in enumerate(self._explored_nodes):
            if node.state not in (self._start.state, self._end.state):
                node.set_color((
                    int(self._start.color[0] + differential[0] * index),
                    int(self._start.color[1] + differential[1] * index),
                    int(self._start.color[2] + differential[2] * index)
                ))

    def _reset_explored_nodes(self) -> None:
        """Resets the count of explored nodes in the maze."""

        for node in self._node_list:
            if node.state == 2:
                node.set_state(1)

        self._reset_optimal_nodes()
        self._count["explored"] = 0
        self._explored_nodes.clear()

    def _reset_optimal_nodes(self) -> None:
        """Resets the count of optimal path nodes in the maze."""

        for node in self._node_list:
            if node.state == 3:
                node.set_state(1)

    def _reset_generated_nodes(self) -> None:
        """Resets the count of generated nodes in the maze."""

        for node in self._node_list:
            if node.state != -10:
                node.set_state(0)

        self._count["path"] = 0

    def _get_neighbors(self, node: Node) -> list:
        """Returns immediate neighbors of a node.

        Gets the nodes immediately next to the given coordinates (top, right,
        bottom, left). If the node is on the edge of the maze, the neighbor
        will be None.

        Note:
        -----
        The order in which the neighbor nodes are returned is set in a random
        way in order to prevent data pre-setting.

        Parameters:
        -----------
         - node: Node
            The node whose neighbors will be returned.
        """

        coordinates = (
            (node.x, node.y - 1),  # Top
            (node.x + 1, node.y),  # Right
            (node.x, node.y + 1),  # Bottom
            (node.x - 1, node.y)   # Left
        )

        self._log(
            f"[NEXT_NODES] Next coordinates for node {node}:",
            coordinates, indentation=1, expand=False
        )

        nodes = [
            self._node_matrix[coord[1]][coord[0]] for coord in coordinates
            if 0 <= coord[0] < self._width and 0 <= coord[1] < self._height
        ]

        nodes = sample(nodes, len(nodes))

        self._log(
            f"[NEXT_NODES] Next nodes for node {node}:", nodes, indentation=2)

        return nodes

    def _get_square_neighbors(self, node: Node) -> list:
        """Returns square neighbors of a node.

        Gets the nodes next to the given coordinates in a square (top-left,
        top, top-right, right, bottom-right...). If the node is on the edge of
        the maze, the neighbor will be None.

        Since the method is only used to evaluate the amount of nearby 'path'
        values near the considered node during path generation, there is no
        point in returning a randomized sample.
        """

        coordinates = (
            (node.x - 1, node.y - 1),
            (node.x, node.y - 1),
            (node.x + 1, node.y - 1),
            (node.x + 1, node.y),
            (node.x + 1, node.y + 1),
            (node.x, node.y + 1),
            (node.x - 1, node.y + 1),
            (node.x - 1, node.y)
        )

        self._log(
            f"[SURROUNDING NODES] Surrounding coordinates for node {node}:",
            coordinates, indentation=1, expand=False
        )

        nodes = [
            self._node_matrix[coord[1]][coord[0]] for coord in coordinates
            if 0 <= coord[0] < self._width and 0 <= coord[1] < self._height
        ]

        self._log(
            f"[SURROUNDING NODES] Surrounding nodes for node {node}: ", nodes, indentation=2)

        return nodes

    def _get_optimal_path(self) -> None:
        """Determines the optimal path from the end to the start node.

        This process is performed by reversing the search process and
        evaluating each node's parent. The parent of the start node is None,
        so the process stops when the start is reached.
        """

        if self._end in self._explored_nodes:
            self.optimal_path = [self._end]
            node = self._end.parent

            while node.parent is not None:
                self.optimal_path.append(node)
                node.set_state(3, set_color=False)
                node = node.parent

            self.optimal_path.append(self._start)
            self.optimal_path.reverse()

    def _randomize_divergence(self, nodes: list) -> list:
        """Randomizes the divergence during path generation process."""

        self._log("[CAESAR] Unfiltered:", nodes, indentation=1)

        bias = round(max(self._width, self._height) * (1 / 4))
        chance = randint(bias if bias <= len(
            nodes) else len(nodes), len(nodes))
        nodes = sample(nodes, chance if 0 <= chance <=
                       len(nodes) else .66 * len(nodes))

        self._log("[CAESAR] Filtered:", nodes, indentation=2)

        return nodes

    def _set_end_node(self, probability=1) -> None:
        """Sets the location of the end node.

        Parameters:
        -----------
         - probability: float (defaul=1)
            The probability of the end node being set.
        """

        if not 0 <= probability <= 1:
            raise TypeError("'probability' must be a float between 0 and 1.")

        if randint(0, 100) / 100 < probability:
            path_tiles = [node for node in self._node_list if node.state == 1]

            self._log("[GOAL SPREADER] Elements:", path_tiles, indentation=1)

            self._end = path_tiles[0]
            top_distance = self.manhattan_distance(self._end, path_tiles[0])

            for tile in path_tiles:
                if self.manhattan_distance(self._start, tile) > top_distance:
                    top_distance = self.manhattan_distance(self._start, tile)
                    self._end = tile

            self._end.set_state(10)

            self._log("[GOAL SPREADER] Selected goal:",
                      self._end, indentation=2)

    def _generate_path(self) -> None:
        """Generates a random path for the base array."""

        if self._is_generated:
            self._reset_generated_nodes()

        self._log("Start:", self._start)
        timer = time()
        frontier = [self._start]

        self._log("[PATH GENERATOR] Initial rontier:", frontier)

        while frontier:
            selected_nodes, candidates = [], []

            for node in frontier:
                candidates.extend(
                    [neighbor for neighbor in self._get_neighbors(node)
                     if neighbor.state not in (-10, 1)]
                )

            self._log("[PATH GENERATOR] Candidates:", candidates)

            selected_nodes = self._randomize_divergence([
                candidate for candidate in candidates if len([
                    node for node in self._get_square_neighbors(candidate)
                    if self._node_matrix[node.y][node.x].state in (-10, 1)
                ]) <= 2
            ])

            # FIXME: this might be the cause of the lack of divergence.
            frontier = selected_nodes
            for node in frontier:
                node.set_state(1)
                self._count["path"] += 1

            self._log("[PATH GENERATOR] Updated frontier:", frontier)
            self._log(f"[PATH GENERATOR] Updated display:\n\n{self.ascii()}")

        self._log("[PATH GENERATOR] Node map:", self._node_list)

        self._set_end_node()
        self._is_generated = True

        self._log("[PATH GENERATOR] Generation time:",
                  f"{(time() - timer):.5f}s.")
        self._log(f"Display:\n{str(self)}", indentation=1)

    def ascii(self) -> str:
        """Returns an ASCII representation of the maze array.

        Each node is represented by a character, given its state.
        """

        return (f"╔═{2 * '═' * self._width}╗\n"
                + ''.join(
                    ''.join(
                        ['║ ' + ''.join(
                            [node.ascii for node in row]
                        ) + '║\n']
                    ) for row in self._node_matrix
                ) + f"╚═{2 * '═' * self._width}╝"
                )

    def image(self, show_image=True, save_image=False) -> str:
        """Generates an image from the maze array with colored nodes.

        Parameters:
        -----------
         - show_image : bool
            Determines whether or not the image should be displayed.
         - save_image : bool
            Determines whether or not the image should be saved.
        """

        # Dimensions and canvas definition:
        cell, border = 50, 8

        image = Image.new(
            mode="RGB", size=(self._width * cell, self._height * cell), color="black"
        )

        # Canvas modification:
        image_draw = ImageDraw.Draw(image)

        for ri, row in enumerate(self._node_matrix):
            for ci, node in enumerate(row):
                if node.state in (-10, 3, 10):
                    if node.state == 3:
                        pre_border = border
                        pattern_fill = (
                            int(node.color[0] + .5 * node.color[0]),
                            int(node.color[1] + .5 * node.color[1]),
                            int(node.color[2] + .5 * node.color[2])
                        )
                    else:
                        pre_border = border
                        pattern_fill = (
                            int(node.color[0] + 2 * node.color[0]),
                            int(node.color[1] + 2 * node.color[1]),
                            int(node.color[2] + 2 * node.color[2])
                        )

                    image_draw.rectangle((
                        (ci * cell + pre_border // 2, ri * cell + pre_border // 2),
                        ((ci + 1) * cell - pre_border // 2,
                         (ri + 1) * cell - pre_border // 2)
                    ),
                        fill=pattern_fill
                    )

                image_draw.rectangle((
                    (ci * cell + border, ri * cell + border),
                    ((ci + 1) * cell - border,
                     (ri + 1) * cell - border)
                ),
                    fill=node.color
                )

        # Image export:
        if show_image:
            image.show()

        if save_image:
            if not path.isdir(f"./{self.IMAGE_DIRECTORY}"):
                mkdir(f"./{self.IMAGE_DIRECTORY}")

            self.IMAGE_FILE = f"./{self.IMAGE_DIRECTORY}/{self.IMAGE_PREFIX}" \
                + f"_{''.join(str(time()).split('.'))}.{self.IMAGE_FORMAT}"

            image.save(self.IMAGE_FILE)

            return self.IMAGE_FILE

        return ''

    def __repr__(self):
        return f"<({self._width}x{self._height}) Maze instance>"

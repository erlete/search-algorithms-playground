from datetime import datetime
from os import mkdir, path
from random import randint, randrange, sample
from time import time
from PIL import Image, ImageDraw
from utils.node import Node

from utils.frontier import StackFrontier, QueueFrontier

class MazeBase:
    """Contains the methods and attributes related to maze generation.
    """

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

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

        self._x, self._y = self._dimensions  # Unpacks the tuple.

    def __init__(self, dimensions, logger=False):

        self.dimensions = dimensions

        # Maze generation process:
        self._node_matrix = [
            [Node(column, row) for column in range(self._x)]
            for row in range(self._y)
        ]

        self._node_list = [node for row in self._node_matrix for node in row]

        self._start = self._node_matrix[
            randrange(0, self._y)
        ][randrange(0, self._x)]
        self._start.set_state(-10)
        self._end = Node(0, 0)

        # Maze statistics initialization:
        self._explored_nodes, self.optimal_path = [], []
        self._is_generated = self._is_explored = False
        self._count = {
            "path": 0,
            "explored": 0,
            "total": self._x * self._y
        }


class Maze(MazeBase):
    """The base class for the maze generation and representation. Provides
    with generator, solver and display methods for node treatment and
    arrangement.

    Parameters
    ----------
    dimensions : int | tuple[int, int]
        Integer or 2-tuple of integers defining the X and Y dimensions (width
        and height) of the node array.
    logger : bool
        Flag that determines whether or not the processes performed by the
        class' methods should be logged.
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
        """TODO: add docstring"""

        differential = (
            (self._end.color[0] - self._start.color[0]) /
            self._count["explored"],
            (self._end.color[1] - self._start.color[1]) /
            self._count["explored"],
            (self._end.color[2] - self._start.color[2]) /
            self._count["explored"],
        )

        for index, node in enumerate(self._explored_nodes):
            if node.state not in (self._start.state, self._end.state):
                node.set_color((
                    int(self._start.color[0] + differential[0] * index),
                    int(self._start.color[1] + differential[1] * index),
                    int(self._start.color[2] + differential[2] * index)
                ))

    def _reset_explored_nodes(self) -> None:
        """TODO: add docstring"""

        for node in self._node_list:
            if node.state == 2:
                node.set_state(1)

        self._reset_optimal_nodes()
        self._count["explored"] = 0
        self._explored_nodes.clear()

    def _reset_optimal_nodes(self) -> None:
        """TODO: add docstring"""

        for node in self._node_list:
            if node.state == 3:
                node.set_state(1)

    def _reset_generated_nodes(self) -> None:
        """TODO: add docstring"""

        for node in self._node_list:
            if node.state != -10:
                node.set_state(0)

        self._count["path"] = 0

    def _get_neighbors(self, node: Node) -> list:
        """Gets the nodes immediately next to the given coordinates from
        `self.node_matrix` (top, right, bottom, left).

        The order in which the neighbor nodes are returned is set in a random
        way, in order to prevent data pre-setting.
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
            if 0 <= coord[0] < self._x and 0 <= coord[1] < self._y
        ]
        nodes = sample(nodes, len(nodes))

        self._log(
            f"[NEXT_NODES] Next nodes for node {node}:", nodes, indentation=2)

        return nodes

    def _get_square_neighbors(self, node: Node) -> list:
        """Gets the values in the square surroundings of the given coordinates.
        This method is used in order to prevent path mixing during generation.

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
            if 0 <= coord[0] < self._x and 0 <= coord[1] < self._y
        ]

        self._log(
            f"[SURROUNDING NODES] Surrounding nodes for node {node}: ", nodes, indentation=2)

        return nodes

    def _get_optimal_path(self) -> None:
        """TODO: add docstring"""

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
        """TODO: add docstring"""

        self._log("[CAESAR] Unfiltered:", nodes, indentation=1)

        bias = round(max(self._x, self._y) * (1 / 4))
        chance = randint(bias if bias <= len(
            nodes) else len(nodes), len(nodes))
        nodes = sample(nodes, chance if 0 <= chance <=
                       len(nodes) else .66 * len(nodes))

        self._log("[CAESAR] Filtered:", nodes, indentation=2)

        return nodes

    def _set_end_node(self, probability=.8) -> None:
        """TODO: add docstring"""

        if not 0 <= probability <= 1:
            raise TypeError("'probability' must be a float between 0 and 1.")

        if randint(0, 100) / 100 < probability:
            path_tiles = [node for node in self._node_list if node.state == 1]

            self._log("[GOAL SPREADER] Elements:", path_tiles, indentation=1)

            self._end = path_tiles[0]
            top_distance = self._manhattan_distance(self._end, path_tiles[0])

            for tile in path_tiles:
                if self._manhattan_distance(self._start, tile) > top_distance:
                    top_distance = self._manhattan_distance(self._start, tile)
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

    @staticmethod
    def _manhattan_distance(start: Node, end: Node) -> int:
        """Returns the _manhattan_distance distance between two nodes (sum of
        the absolute cartesian coordinates difference between two nodes).

        Parameters
        ----------
        start : Node
                The starting node.
        end : Node
                The ending node.
        """

        return abs(start.x - end.x) + abs(start.y - end.y)

    @staticmethod
    def _radial_distance(start: Node, end: Node) -> float:
        """Returns the radial distance distance between two nodes (square root
        of the sum of each node's coordinates squared).

        Parameters
        ----------
        start : Node
                The starting node.
        end : Node
                The ending node.
        """
        return ((start.x - end.x) ** 2 + (start.y - end.y) ** 2) ** .5

    def depth_first_search(self) -> bool:
        """Depth-First Search method."""

        if self._is_explored:
            self._reset_explored_nodes()

        timer = time()
        frontier = StackFrontier(self._start)
        self._is_explored, has_end = True, False

        self._log("[DFS] Initial frontier:", frontier)

        while not frontier.is_empty() and not has_end:
            self._explored_nodes.append(node := frontier.remove_node())
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

            frontier.add_nodes(neighbors)

            self._log("[DFS] Updated frontier:", frontier)

        self._count["explored"] = len(self._explored_nodes)
        self._set_node_color()
        self._get_optimal_path()
        return has_end

    def breadth_first_search(self) -> bool:
        """Breadth-First Search method."""

        if self._is_explored:
            self._reset_explored_nodes()

        timer = time()
        frontier = QueueFrontier(self._start)
        self._is_explored, has_end = True, False

        self._log("[BFS] Initial frontier:", frontier)

        while not frontier.is_empty() and not has_end:
            self._explored_nodes.append(node := frontier.remove_node())
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

            frontier.add_nodes(neighbors)

            self._log("[BFS] Updated frontier:", frontier)

        self._count["explored"] = len(self._explored_nodes)
        self._set_node_color()
        self._get_optimal_path()
        return has_end

    def greedy_best_first_search(self) -> bool:
        """Greedy Best-First Search method."""

        if self._is_explored:
            self._reset_explored_nodes()

        for node in self._node_list:
            node.weight = self._manhattan_distance(node, self._end)

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
        """Radial Search method."""

        if self._is_explored:
            self._reset_explored_nodes()

        for node in self._node_list:
            node.weight = self._radial_distance(node, self._end)

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

    def ascii(self) -> str:
        """Returns an ASCII representation of the maze array with each node's
        corresponding character.
        """
        return (f"╔═{2 * '═' * self._x}╗\n"
                + ''.join(
                    ''.join(
                        ['║ ' + ''.join(
                                [node.ascii for node in row]
                        ) + '║\n']
                    ) for row in self._node_matrix
                ) + f"╚═{2 * '═' * self._x}╝"
                )

    def image(self, *, show_image=True, save_image=False) -> str:
        """Generates an image from the maze array, coloring each
        node in a different way.

        Parameters
        ----------
        show_image : bool
                Determines whether or not the image should be displayed.
        save_image : bool
                Determines whether or not the image should be saved.
        """
        # Dimensions and canvas definition:
        cell, border = 50, 8

        image = Image.new(
            mode="RGB", size=(self._x * cell, self._y * cell), color="black"
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
        return f"<({self._x}x{self._y}) Maze instance>"
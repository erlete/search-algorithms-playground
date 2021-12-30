"""Main generator and solver module for search algorithms testing."""


from datetime import datetime
from PIL import Image, ImageDraw
from random import randint, randrange, sample
from os import mkdir, path
from time import time


class Node:
	"""Data structure that represents an element of an array with special
	properties.

	Parameters
	----------
	x : int
		X axis coordinate (matrix row).
	y : int
		Y axis coordinate (matrix column).
	state : int
		Value that defines the node's qualities (0: wall, 1: path...).
	weight : int
		Value that measures how much the overall path cost increases when the
		node is considered as part of it.
	parent : Node
		Another node from which the current one is origined.
	color : tuple[int, int, int]
		RGB color code for visual display of the node.
	"""

	STATE_STRING = {
		-10: "Start",
		0: "Wall",
		1: "Path",
		2: "Explored",
		3: "Optimal",
		10: "End"
	}

	STATE_ASCII = {
		-10: 'A ',
		0: '█ ',
		1: '  ',
		2: '░ ',
		3: 'o ',
		10: 'B '
	}

	STATE_COLOR = {
		-10: (166, 47, 47),
		0: (0, 0, 0),
		1: (200, 200, 200),
		2: (0, 0, 0),
		3: (235, 167, 89),
		10: (48, 19, 92)
	}

	def __init__(self, x: int, y: int, state=0, weight=0, parent=None):
		# Node localization:
		self.x, self.y = x, y
		self.parent = parent

		# Node classification:
		self.state = state
		self.weight = weight

		# Display:
		self.color = self.STATE_COLOR[self.state]
		self.ascii = self.STATE_ASCII[self.state]

	def set_state(self, state: int, set_color=True, set_ascii=True) -> None:
		"""Changes node's state and its linked attributes."""
		self.state = state
		if set_color:
			self.color = self.STATE_COLOR[self.state]
		if set_ascii:
			self.ascii = self.STATE_ASCII[self.state]

	def set_color(self, rgb: tuple[int, int, int]) -> None:
		"""Changes node's color."""
		self.color = rgb

	def __repr__(self):
		return f"Node(X: {self.x}, Y: {self.y}, " \
		+ f"S: {self.STATE_STRING[self.state]:10s}, W: {self.weight})"


class Frontier:
	"""Data structure that contains nodes."""
	def __init__(self, initial_node: Node):
		self.nodes = [initial_node]

	def add_nodes(self, nodes: list[Node]) -> None:
		self.nodes.extend(nodes)

	def is_empty(self) -> bool:
		return len(self.nodes) == 0

	def __repr__(self):
		return f"{self.nodes}"


class StackFrontier(Frontier):
	"""Frontier expansion that removes nodes via LIFO."""
	def remove_node(self) -> None:
		return self.nodes.pop()


class QueueFrontier(Frontier):
	"""Frontier expansion that removes nodes via FIFO."""
	def remove_node(self) -> None:
		return self.nodes.pop(0)


class Maze:
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
		if isinstance(dimensions, tuple):
			if dimensions[0] <= 3 or dimensions[1] <= 3:
				raise Exception("'dimensions' must be greater than 3.")
		elif isinstance(dimensions, int):
			if dimensions <= 3:
				raise Exception("'dimensions' must be greater than 3.")
			dimensions = (dimensions, dimensions)
		else:
			raise Exception("'dimensions' must be 'tuple' or 'int'.")

		# Array configuration:
		self.x, self.y = dimensions[0], dimensions[1]

		self.node_matrix = [
			[Node(column, row) for column in range(self.x)]
			for row in range(self.y)
		]
		self.node_list = [node for row in self.node_matrix for node in row]

		self.start = self.node_matrix[randrange(0, self.y)][randrange(0, self.x)]
		self.start.set_state(-10)

		# Array metrics:
		self.explored_nodes, self.optimal_path = [], []
		self.is_generated = self.is_explored = False
		self.count = {
			"path": 0,
			"explored": 0,
			"total": self.x * self.y
		}

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

		self.path_generator()


	def _writer(self, file: str, argument, indentation: int, newlines: int):
		header = f"+ {datetime.now().isoformat()} "
		file.write(
			header.ljust(len(header) + 4 * (indentation + 1), '-')
			+ f" {argument}" + newlines * '\n'
		)


	def _log(self, *arguments, indentation=0, expand=True) -> None:
		if not self.logger:
			return None

		if not path.isdir(f"./{self.LOG_DIRECTORY}"):
			mkdir(f"./{self.LOG_DIRECTORY}")

		with open(self.LOG_FILE, mode='a') as lg:
			if len(arguments) >= 1:
				self._writer(lg, arguments[0], indentation, 1)

				if len(arguments) > 1:
					for argument in arguments[1:]:
						if isinstance(argument, (list, tuple, set)) and expand:
							for index, element in enumerate(argument):
								self._writer(lg, f"{index} :: {element}", indentation + 2, 1)
						else:
							self._writer(lg, argument, indentation + 1, 1)

			lg.write('\n')


	def _set_node_color(self):
		differential = (
			(self.end.color[0] - self.start.color[0]) / self.count["explored"],
			(self.end.color[1] - self.start.color[1]) / self.count["explored"],
			(self.end.color[2] - self.start.color[2]) / self.count["explored"],
		)
		for index, node in enumerate(self.explored_nodes):
			if node.state not in (self.start.state, self.end.state):
				node.set_color((
					int(self.start.color[0] + differential[0] * index),
					int(self.start.color[1] + differential[1] * index),
					int(self.start.color[2] + differential[2] * index)
				))


	def _reset_explored_nodes(self) -> None:
		for node in self.node_list:
			if node.state == 2:
				node.set_state(1)

		self._reset_optimal_nodes()
		self.count["explored"] = 0
		self.explored_nodes.clear()


	def _reset_optimal_nodes(self) -> None:
		for node in self.node_list:
			if node.state == 3:
				node.set_state(1)


	def _reset_generated_nodes(self) -> None:
		for node in self.node_list:
			if node.state != -10:
				node.set_state(0)

		self.count["path"] = 0


	def _get_neighbors(self, node: Node) -> list:
		"""Gets the nodes immediately next to the given coordinates from
		'self.node_matrix'.

		The order in which the surrounding nodes are returned is set in a
		random way, in order to prevent data pre-setting.

		Process illustration:
		---------------------

				T
			L   X   R
				B
		"""

		coordinates = (
			(node.x, node.y - 1),  # Top
			(node.x + 1, node.y),  # Right
			(node.x, node.y + 1),  # Bottom
			(node.x - 1, node.y)   # Left
		)

		self._log(f"[NEXT_NODES] Next coordinates for node {node}:", coordinates, indentation=1, expand=False)

		nodes = [
			self.node_matrix[coord[1]][coord[0]] for coord in coordinates
			if 0 <= coord[0] < self.x and 0 <= coord[1] < self.y
		]
		nodes = sample(nodes, len(nodes))

		self._log(f"[NEXT_NODES] Next nodes for node {node}:", nodes, indentation=2)

		return nodes


	def _get_square_neighbors(self, node: Node) -> list:
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
			(node.x - 1, node.y - 1),  # Top left
			(node.x, node.y - 1),	  # Top center
			(node.x + 1, node.y - 1),  # Top right
			(node.x + 1, node.y),	  # Middle right
			(node.x + 1, node.y + 1),  # Bottom right
			(node.x, node.y + 1),	  # Bottom center
			(node.x - 1, node.y + 1),  # Bottom left
			(node.x - 1, node.y)	   # Middle left
		)

		self._log(f"[SURROUNDING NODES] Surrounding coordinates for node {node}:", coordinates, indentation=1, expand=False)

		nodes = [
			self.node_matrix[coord[1]][coord[0]] for coord in coordinates
			if 0 <= coord[0] < self.x and 0 <= coord[1] < self.y
		]

		self._log(f"[SURROUNDING NODES] Surrounding nodes for node {node}: ", nodes, indentation=2)

		return nodes


	def _get_optimal_path(self) -> None:
		if self.end in self.explored_nodes:
			self.optimal_path = [self.end]
			node = self.end.parent
			while node.parent is not None:
				self.optimal_path.append(node)
				node.set_state(3, set_color=False)
				node = node.parent
			self.optimal_path.append(self.start)
			self.optimal_path.reverse()


	def _randomize_divergence(self, nodes: list) -> list:
		"""Random path divergence generator. Takes one or multiple path
		divergence possibilities and selects at least one of them.

		The name is due to the 'lives, dies' choice of Julius Caesar during
		colosseum gladiator games.
		"""
		self._log("[CAESAR] Unfiltered:", nodes, indentation=1)

		bias = round(max(self.x, self.y) * (1 / 4))
		chance = randint(bias if bias <= len(nodes) else len(nodes), len(nodes))
		nodes = sample(nodes, chance if 0 <= chance <= len(nodes) else .66 * len(nodes))

		self._log("[CAESAR] Filtered:", nodes, indentation=2)

		return nodes


	def _set_end_node(self) -> None:
		"""Sets the position of the goal state at the farthest possible
		coordinate in the array.
		"""

		path_tiles = [node for node in self.node_list if node.state == 1]

		self._log("[GOAL SPREADER] Elements:", path_tiles, indentation=1)

		self.end = path_tiles[0]
		top_distance = self._manhattan_distance(self.end, path_tiles[0])

		for tile in path_tiles:
			if self._manhattan_distance(self.start, tile) > top_distance:
				top_distance = self._manhattan_distance(self.start, tile)
				self.end = tile

		self.end.set_state(10)

		self._log("[GOAL SPREADER] Selected goal:", self.end, indentation=2)


	def path_generator(self, bias=5) -> None:
		"""Randomly generates a pathway for the array."""

		if self.is_generated:
			self._reset_generated_nodes()

		self._log("Start:", self.start)
		timer = time()
		frontier = [self.start]

		self._log("[PATH GENERATOR] Initial rontier:", frontier)

		while frontier != []:
			selected_nodes, candidates = [], []

			for index, node in enumerate(frontier):
				candidates.extend(
					[neighbor for neighbor in self._get_neighbors(node)
					if neighbor.state not in (-10, 1)]
				)

			self._log("[PATH GENERATOR] Candidates:", candidates)

			selected_nodes = self._randomize_divergence([
				candidate for candidate in candidates if len([
					node for node in self._get_square_neighbors(candidate)
					if self.node_matrix[node.y][node.x].state in (-10, 1)
				]) <= 2
			])

			frontier = selected_nodes  # FIXME: this might be the cause of the lack of divergence.
			for node in frontier:
				node.set_state(1)
				self.count["path"] += 1

			self._log("[PATH GENERATOR] Updated frontier:", frontier)
			self._log(f"[PATH GENERATOR] Updated display:\n\n{self.ascii()}")

		self._log("[PATH GENERATOR] Node map:", self.node_list)

		self._set_end_node()
		self.is_generated = True

		self._log("[PATH GENERATOR] Generation time:", f"{(time() - timer):.5f}s.")
		self._log(f"Display:\n{str(self)}", indentation=1)


	@staticmethod
	def _manhattan_distance(start: Node, end: Node) -> int:
		"""Returns the _manhattan_distance distance between two nodes (sum of the
		absolute cartesian coordinates difference between two nodes).
		"""
		return abs(start.x - end.x) + abs(start.y - end.y)


	@staticmethod
	def _radial_distance(start: Node, end: Node) -> float:
		"""Returns the _radial_distance distance between two nodes (square root of the
		sum of each node's coordinates squared).
		"""
		return ((start.x - end.x) ** 2 + (start.y - end.y) ** 2) ** .5


	def dfs(self) -> bool:
		"""Depth-First Search (DFS)."""

		if self.is_explored:
			self._reset_explored_nodes()

		timer = time()
		frontier = StackFrontier(self.start)
		self.is_explored, has_end = True, False

		self._log("[DFS] Initial frontier:", frontier)

		while not frontier.is_empty() and not has_end:
			self.explored_nodes.append(node := frontier.remove_node())
			if node.state != -10:
				node.set_state(2)

			self._log("[DFS] Selected node:", node)
			self._log(f"[DFS] Updated display:\n\n{self.ascii()}")

			neighbors = [node for node in self._get_neighbors(node) if node.state in (1, 10)]

			for neighbor in neighbors:
				neighbor.parent = node

				if neighbor.state == self.end.state:
					self.explored_nodes.append(self.end)
					has_end = True

					self._log("[DFS] Search time:", f"{(time() - timer):.5}s.")
					break

			frontier.add_nodes(neighbors)

			self._log("[DFS] Updated frontier:", frontier)

		self.count["explored"] = len(self.explored_nodes)
		self._set_node_color()
		self._get_optimal_path()
		return has_end


	def bfs(self) -> bool:
		"""Breadth-First Search (BFS)."""

		if self.is_explored:
			self._reset_explored_nodes()

		timer = time()
		frontier = QueueFrontier(self.start)
		self.is_explored, has_end = True, False

		self._log("[BFS] Initial frontier:", frontier)

		while not frontier.is_empty() and not has_end:
			self.explored_nodes.append(node := frontier.remove_node())
			if node.state != -10:
				node.set_state(2)

			self._log("[BFS] Selected node:", node)
			self._log(f"[BFS] Updated display:\n\n{self.ascii()}")

			neighbors = [node for node in self._get_neighbors(node) if node.state in (1, 10)]

			for neighbor in neighbors:
				neighbor.parent = node

				if neighbor.state == self.end.state:
					self.explored_nodes.append(self.end)
					has_end = True

					self._log("[BFS] Search time:", f"{(time() - timer):.5}s.")
					break

			frontier.add_nodes(neighbors)

			self._log("[BFS] Updated frontier:", frontier)

		self.count["explored"] = len(self.explored_nodes)
		self._set_node_color()
		self._get_optimal_path()
		return has_end


	def gbfs(self) -> bool:
		"""Greedy Best-First Search (GBFS)."""

		if self.is_explored:
			self._reset_explored_nodes()

		for node in self.node_list:
			node.weight = self._manhattan_distance(node, self.end)

		timer = time()
		frontier = [self.start]
		self.is_explored, has_end = True, False

		self._log("[GBFS] Initial frontier:", frontier)

		while len(frontier) >= 1 and not has_end:
			self.explored_nodes.append(node := frontier.pop())
			if node.state != -10:
				node.set_state(2)

			self._log("[GBFS] Selected node:", node)
			self._log(f"[GBFS] Updated display:\n\n{self.ascii()}")

			neighbors = [node for node in self._get_neighbors(node) if node.state in (1, 10)]

			for neighbor in neighbors:
				neighbor.parent = node

				if neighbor.state == self.end.state:
					self.explored_nodes.append(self.end)
					has_end = True

					self._log("[GBFS] Search time:", f"{(time() - timer):.5f}s.")
					break

			self._log("[GBFS] Neighbors:", neighbors, indentation=1)

			frontier.extend(neighbors)
			frontier = sorted(frontier, reverse=True, key=lambda x: x.weight)

			self._log("[GBFS] Updated frontier:", frontier)

		self.count["explored"] = len(self.explored_nodes)
		self._set_node_color()
		self._get_optimal_path()
		return has_end


	def rs(self) -> bool:
		"""Radial Search (GBFS)."""

		if self.is_explored:
			self._reset_explored_nodes()

		for node in self.node_list:
			node.weight = self._radial_distance(node, self.end)

		timer = time()
		frontier = [self.start]
		self.is_explored, has_end = True, False

		self._log("[RS] Initial frontier:", frontier)

		while len(frontier) >= 1 and not has_end:
			self.explored_nodes.append(node := frontier.pop())
			if node.state != -10:
				node.set_state(2)

			self._log("[RS] Selected node:", node)
			self._log(f"[RS] Updated display:\n\n{self.ascii()}")

			neighbors = [node for node in self._get_neighbors(node) if node.state in (1, 10)]

			for neighbor in neighbors:
				if neighbor.state == self.end.state:
					self.explored_nodes.append(self.end)
					has_end = True

					self._log("[RS] Search time:", f"{(time() - timer):.5f}s.")
					break

			self._log("[RS] Neighbors:", neighbors, indentation=1)

			frontier.extend(neighbors)
			frontier = sorted(frontier, reverse=True, key=lambda x: x.weight)

			self._log("[RS] Updated frontier:", frontier)

		self.count["explored"] = len(self.explored_nodes)
		self._set_node_color()
		self._get_optimal_path()
		return has_end



	def ascii(self) -> str:
		return (
			f"╔═{2 * '═' * self.x}╗\n"
				+ ''.join(
					''.join(
						['║ ' + ''.join(
							[node.ascii for node in row]
						) + '║\n']
					) for row in self.node_matrix
				) + f"╚═{2 * '═' * self.x}╝"
			)


	def image(self, show_image=True, save_image=False) -> None:

		# Dimensions and canvas definition:
		cell, border = 50, 8

		image = Image.new(
			mode="RGB", size=(self.x * cell, self.y * cell), color="black"
		)

		# Canvas modification:
		image_draw = ImageDraw.Draw(image)

		for ri, row in enumerate(self.node_matrix):
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
							((ci + 1) * cell - pre_border // 2, (ri + 1) * cell - pre_border // 2)
						),
						fill=pattern_fill
					)

				image_draw.rectangle((
						(ci * cell + border, ri * cell + border),
						((ci + 1) * cell - border, (ri + 1) * cell - border)
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


	def __repr__(self):
		return f"({self.x}x{self.y}) {self.__class__} instance"

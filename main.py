"""Main generator and solver module for search algorithms testing."""


from datetime import datetime
from math import log
from PIL import Image, ImageDraw
from random import randint, randrange, sample
from os import mkdir, path
from time import time


class Node:
	def __init__(self, x: int, y: int, state=0, weight=0, color=(0, 0, 0)):
		# Spatial attributes:
		self.X, self.Y = x, y
		self.coordinates = (x, y)

		# Qualitative attributes:
		self.weight = weight
		self.state = state
		self.color = color


	def __repr__(self):
		return f"(X: {self.X}, Y: {self.Y}, S: {self.state}, W: {self.weight})"


class Maze:
	"""This class generates a blank array of (m x n) dimensions, made of '0'
	values, stored in the 'Base' attribute.

	Given that array, an algorithm generates a 'path', made out of '1' values,
	which later on can be evaluated by a search algorithm in order to explore
	the path. Explored nodes have a numerical value of '2'.

	The initial and goal states are represented by '-10' and '10' values,
	respectively.
	"""

	def __init__(self, dimensions=(10, 10), logger=False):
		if not isinstance(dimensions, tuple):
			raise Exception("Dimensions must be a 2-tuple.")
		if (dimensions[0] + dimensions[1]) / 2 <= 1:
			raise Exception("Dimensions' values must be greater than one.")

		# Image output:
		self.start_color = (82, 84, 169)
		self.end_color = (80, 210, 110)
		self.wall_color = (0, 0, 0)
		self.path_color = (175, 175, 175)
		self.explored_color = (
			self.start_color[0],
			self.start_color[1],
			self.start_color[2]
		)

		self.r_diff, self.g_diff, self.b_diff = 0, 0, 0

		# Array settings:
		self.X, self.Y = dimensions[0], dimensions[1]

		self.base = [
			[Node(column, row, state=0, color=self.wall_color)
			for column in range(self.X)] for row in range(self.Y)
		]

		self.start = self.base[randrange(0, self.Y)][randrange(0, self.X)]
		self.start.state, self.start.color = -10, self.start_color

		# Plain node array:
		self.node_map = []
		for row in self.base:
			self.node_map.extend(row)

		# Array statistics:
		self.total_count = self.X * self.Y
		self.path_count, self.explored_count = 0, 0

		self.is_pathed, self.is_explored = False, False

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
		#	the necessity of making its identifier variable (in 'Maze.image').

		self.path_generator()


	def writer(self, file: str, argument, indentation: int, newlines: int):
		header = f"+ {datetime.now().isoformat()} "
		file.write(
			header.ljust(len(header) + 4 * (indentation + 1), '-')
			+ f" {argument}" + newlines * '\n'
		)


	def log(self, *arguments, indentation=0, expand=True) -> None:
		if not self.logger:
			return None

		if not path.isdir(f"./{self.LOG_DIRECTORY}"):
			mkdir(f"./{self.LOG_DIRECTORY}")

		with open(self.LOG_FILE, mode='a') as lg:
			if len(arguments) >= 1:
				self.writer(lg, arguments[0], indentation, 1)

				if len(arguments) > 1:
					for argument in arguments[1:]:
						if isinstance(argument, (list, tuple, set)) and expand:
							for index, element in enumerate(argument):
								self.writer(lg, f"{index} :: {element}", indentation + 2, 1)
						else:
							self.writer(lg, argument, indentation + 1, 1)

			lg.write('\n')


	def set_gradient(self, total_explored_nodes: int) -> None:
		self.r_diff = (self.end_color[0] - self.start_color[0]) / total_explored_nodes
		self.g_diff = (self.end_color[1] - self.start_color[1]) / total_explored_nodes
		self.b_diff = (self.end_color[2] - self.start_color[2]) / total_explored_nodes


	def increment_gradient(self) -> None:
		self.explored_color = (
			self.explored_color[0] + self.r_diff,
			self.explored_color[1] + self.g_diff,
			self.explored_color[2] + self.b_diff
		)


	def set_node_color(self, explored_nodes: int) -> None:
		for node in explored_nodes:
			self.increment_gradient()
			node.color = (
				round(self.explored_color[0]),
				round(self.explored_color[1]),
				round(self.explored_color[2])
			)


	def next_nodes(self, node: Node) -> list:
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

		self.log(f"[NEXT_NODES] Next coordinates for node {node}:", coordinates, indentation=1, expand=False)

		nodes = [
			self.base[coord[1]][coord[0]] for coord in coordinates
			if 0 <= coord[0] < self.X and 0 <= coord[1] < self.Y
		]
		nodes = sample(nodes, len(nodes))

		self.log(f"[NEXT_NODES] Next nodes for node {node}:", nodes, indentation=2)

		return nodes


	def surrounding_nodes(self, node: Node) -> list:
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
			(node.X, node.Y - 1),	  # Top center
			(node.X + 1, node.Y - 1),  # Top right
			(node.X + 1, node.Y),	  # Middle right
			(node.X + 1, node.Y + 1),  # Bottom right
			(node.X, node.Y + 1),	  # Bottom center
			(node.X - 1, node.Y + 1),  # Bottom left
			(node.X - 1, node.Y)	   # Middle left
		)

		self.log(f"[SURROUNDING NODES] Surrounding coordinates for node {node}:", coordinates, indentation=1, expand=False)

		nodes = [
			self.base[coord[1]][coord[0]] for coord in coordinates
			if 0 <= coord[0] < self.X and 0 <= coord[1] < self.Y
		]

		self.log(f"[SURROUNDING NODES] Surrounding nodes for node {node}: ", nodes, indentation=2)

		return nodes


	def clear_explored_nodes(self) -> None:
		for node in self.node_map:
			if node.state == 2:
				node.state = 1
				node.color = self.path_color

		self.explored_count = 0
		self.explored_color = self.start_color


	def clear_pathed_nodes(self) -> None:
		for node in self.node_map:
			if node.state != -10:
				node.state = 0
				node.color = self.wall_color

		self.path_count = 0


	def caesar(self, nodes: list) -> list:
		"""Random path divergence generator. Takes one or multiple path
		divergence possibilities and selects at least one of them.

		The name is due to the 'lives, dies' choice of Julius Caesar during
		colosseum gladiator games.
		"""
		self.log("[CAESAR] Unfiltered:", nodes, indentation=1)

		bias = round(max(self.X, self.Y) * (1 / 4))
		chance = randint(bias if bias <= len(nodes) else len(nodes), len(nodes))
		nodes = sample(nodes, chance if 0 <= chance <= len(nodes) else .66 * len(nodes))

		self.log("[CAESAR] Filtered:", nodes, indentation=2)

		return nodes


	def goal_spreader(self) -> None:
		"""Sets the position of the goal state at the farthest possible
		coordinate in the array.
		"""

		path_tiles = [node for node in self.node_map if node.state == 1]

		self.log("[GOAL SPREADER] Elements:", path_tiles, indentation=1)

		self.end = path_tiles[0]
		top_distance = self.manhattan(self.end, path_tiles[0])

		for tile in path_tiles:
			if self.manhattan(self.start, tile) > top_distance:
				top_distance = self.manhattan(self.start, tile)
				self.end = tile

		self.end.state = 10
		self.end.color = self.end_color

		self.log("[GOAL SPREADER] Selected goal:", self.end, indentation=2)


	def path_generator(self, bias=5) -> None:
		"""Randomly generates a pathway for the array."""

		if self.is_pathed:
			self.clear_pathed_nodes()

		self.log("Start:", self.start)
		timer = time()
		frontier = [self.start]

		self.log("[PATH GENERATOR] Initial rontier:", frontier)

		while frontier != []:
			selected_nodes, candidates = [], []

			for index, node in enumerate(frontier):
				candidates.extend(
					[neighbor for neighbor in self.next_nodes(node)
					if neighbor.state not in (-10, 1)]
				)

			self.log("[PATH GENERATOR] Candidates:", candidates)

			selected_nodes = self.caesar([
				candidate for candidate in candidates if len([
					node for node in self.surrounding_nodes(candidate)
					if self.base[node.Y][node.X].state in (-10, 1)
				]) <= 2
			])

			frontier = selected_nodes
			for node in frontier:
				node.state = 1
				node.color = self.path_color
				self.path_count += 1

			self.log("[PATH GENERATOR] Updated frontier:", frontier)
			self.log(f"[PATH GENERATOR] Updated display:\n\n{self.ascii()}")

		self.log("[PATH GENERATOR] Node map:", self.node_map)

		self.goal_spreader()
		self.is_pathed = True

		self.log("[PATH GENERATOR] Generation time:", f"{(time() - timer):.5f}s.")
		self.log(f"Display:\n{str(self)}", indentation=1)


	@staticmethod
	def manhattan(node_1: Node, node_2: Node) -> int:
		"""Returns the manhattan distance between two nodes (sum of the
		absolute cartesian coordinates difference between two nodes).
		"""
		return abs(node_1.X - node_2.X) + abs(node_1.Y - node_2.Y)


	@staticmethod
	def radial(node_1: Node, node_2: Node) -> float:
		"""Returns the radial distance between two nodes (square root of the
		sum of each node's coordinates squared).
		"""
		return ((node_1.X - node_2.X) ** 2 + (node_1.Y - node_2.Y) ** 2) ** .5


	def dfs(self) -> bool:
		"""Depth-First Search (DFS)."""

		if self.is_explored:
			self.clear_explored_nodes()

		timer = time()
		frontier, explored = self.next_nodes(self.start), []

		self.log("[DFS] Initial frontier:", frontier)

		while len(frontier) >= 1:
			node = frontier.pop()
			explored.append(node)

			node.state = 2 if node.state != -10 else -10
			self.explored_count += 1

			self.log("[DFS] Selected node:", node)

			for neighbor in self.next_nodes(node):
				if neighbor.state == 1:
					frontier.append(neighbor)

					self.log("[DFS] Updated frontier:", frontier)
					self.log(f"[DFS] Updated display:\n\n{self.ascii()}")

				elif neighbor.state == 10:
					self.log("[DFS] Search time:", f"{(time() - timer):.5}s.")

					self.set_gradient(len(explored))
					self.set_node_color(explored)
					self.is_explored = True

					return True

		self.set_gradient(len(explored))
		self.set_node_color(explored)
		self.is_explored = True

		return False


	def gbfs(self) -> bool:
		"""Greedy Best-First Search (GBFS)."""

		if self.is_explored:
			self.clear_explored_nodes()

		for node in self.node_map:
			node.weight = self.manhattan(node, self.end)

		timer = time()
		frontier, explored = [self.start], []

		self.log("[GBFS] Initial frontier:", frontier)

		while len(frontier) >= 1:
			node = frontier.pop()
			explored.append(node)

			node.state = 2 if node.state != -10 else -10
			self.explored_count += 1

			self.log(f"[GBFS] Updated display:\n\n{self.ascii()}")

			candidates = [node for node in self.next_nodes(node) if node.state in (1, 10)]

			if any(candidate.coordinates == self.end.coordinates for candidate in candidates):
				self.log("[GBFS] Search time:", f"{(time() - timer):.5f}s.")

				self.set_gradient(len(explored))
				self.set_node_color(explored)
				self.is_explored = True

				return True

			self.log("[GBFS] Candidates:", candidates, indentation=1)

			frontier.extend(candidates)
			frontier = sorted(frontier, reverse=True, key=lambda x: x.weight)

			self.log("[GBFS] Updated frontier:", frontier)

		self.set_gradient(len(explored))
		self.set_node_color(explored)
		self.is_explored = True

		return False


	def rs(self) -> bool:
		"""Radial Search (GBFS)."""

		if self.is_explored:
			self.clear_explored_nodes()

		for node in self.node_map:
			node.weight = self.radial(node, self.end)

		timer = time()
		frontier, explored = [self.start], []

		self.log("[GBFS] Initial frontier:", frontier)

		while len(frontier) >= 1:
			node = frontier.pop()
			explored.append(node)
			node.state = 2 if node.state != -10 else -10
			self.explored_count += 1

			self.log(f"[RS] Updated display:\n\n{self.ascii()}")

			candidates = [node for node in self.next_nodes(node) if node.state in (1, 10)]

			if any(candidate.coordinates == self.end.coordinates for candidate in candidates):
				timer_end = time()
				self.log("[RS] Search time:", f"{(time() - timer):.5f}s.")

				self.set_gradient(len(explored))
				self.set_node_color(explored)
				self.is_explored = True

				return True

			self.log("[RS] Candidates:", candidates, indentation=1)

			frontier.extend(candidates)
			frontier = sorted(frontier, reverse=True, key=lambda x: x.weight)

			self.log("[RS] Updated frontier:", frontier)

		self.set_gradient(len(explored))
		self.set_node_color(explored)
		self.is_explored = True

		return False


	def ascii(self) -> str:
		ascii_map = {
			-10: 'A ',  # Start
			0: '█ ',	# Wall
			1: '  ',	# Path
			2: '░ ',	# Explored
			10: 'B '	# End
		}

		return (
			f"╔═{2 * '═' * self.X}╗\n"
				+ ''.join(
					''.join(
						['║ ' + ''.join(
							[ascii_map[node.state] for node in row]
						) + '║\n']
					) for row in self.base
				) + f"╚═{2 * '═' * self.X}╝"
			)


	def image(self, show_image=True, save_image=False) -> None:

		# Dimensions and canvas definition:
		cell, border = 50, 4

		image = Image.new(
			mode="RGB", size=(self.X * cell, self.Y * cell), color="black"
		)

		# Canvas modification:
		image_draw = ImageDraw.Draw(image)

		for ri, row in enumerate(self.base):
			for ci, node in enumerate(row):
				image_draw.rectangle(
					([(ci * cell + border, ri * cell + border),
					((ci + 1) * cell - border, (ri + 1) * cell - border)]),
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
		return f"({self.X}x{self.Y}) {self.__class__} instance"

from random import randint, randrange, sample
from time import time
from datetime import datetime
from os import path, mkdir


class Node:
	def __init__(self, x: int, y: int, state=0, weight=0,
			previous_nodes=[], next_nodes=[]):

		# Spatial attributes:
		self.X, self.Y = x, y
		self.coordinates = (x, y)

		# Qualitative attributes:
		self.weight = weight
		self.state = state

		# Node attributes:
		self.previous = previous_nodes
		self.next = next_nodes

	def __repr__(self):
		return f"(X: {self.X}, Y: {self.Y}, S: {self.state})"


class Maze:
	def __init__(self, dimensions=(10, 10), logger=False):
		if not isinstance(dimensions, tuple):
			raise Exception("Dimensions must be a 2-tuple.")
		if (dimensions[0] + dimensions[1]) / 2 <= 1:
			raise Exception("Dimensions' values must be greater than one.")

		# Array settings:
		self.X = dimensions[0]
		self.Y = dimensions[1]
		self.DIMENSIONS = dimensions

		# Bidimensional node array:
		self.base = [
			[Node(column, row, state=0)
			for column in range(self.X)] for row in range(self.Y)
		]

		# Starting point selection:
		self.start = self.base[randrange(0, self.Y)][randrange(0, self.X)]
		self.start.state = -10

		# Plain node array:
		self.node_map = []
		for row in self.base:
			self.node_map.extend(row)

		self.is_explored = False

		# Logger settings:
		self.logger = logger
		self.LOG_DIRECTORY = "logs"
		self.LOG_PREFIX = "log"
		self.LOG_SEPARATOR = '-'
		self.LOG_FILE = f"./{self.LOG_DIRECTORY}/{self.LOG_PREFIX}_" +\
			f"{''.join(str(time()).split('.'))}.txt"


	def writer(self, file: str, argument, indentation: int, newlines: int):
		header = f"+ {datetime.now().isoformat()} "
		file.write(
			header.ljust(
				len(header) + 4 * (indentation + 1), self.LOG_SEPARATOR
			) + f" {argument}" + newlines * '\n'
		)


	def log(self, *arguments, indentation=0, expand=True):
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


	def next_nodes(self, node: Node) -> list:
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

		self.explored_color = self.start_color


	def caesar(self, nodes: list) -> list:
		self.log("[CAESAR] Unfiltered:", nodes, indentation=1)

		bias = round(max(self.X, self.Y) * (1 / 4))
		chance = randint(bias if bias <= len(nodes) else len(nodes), len(nodes))
		nodes = sample(nodes, chance if 0 <= chance <= len(nodes) else .66 * len(nodes))

		self.log("[CAESAR] Filtered:", nodes, indentation=2)

		return nodes


	def goal_spreader(self) -> None:
		path_tiles = [node for node in self.node_map if node.state == 1]

		self.log("[GOAL SPREADER] Elements:", path_tiles, indentation=1)

		self.end = path_tiles[0]
		top_distance = self.manhattan(self.end, path_tiles[0])

		for tile in path_tiles:
			if self.manhattan(self.start, tile) > top_distance:
				top_distance = self.manhattan(self.start, tile)
				self.end = tile

		self.end.state = 10

		self.log("[GOAL SPREADER] Selected goal:", self.end, indentation=2)


	def path_generator(self, bias=5) -> None:
		self.log("Start:", self.start)
		timer_start = time()

		frontier = [self.start]

		self.log("[PATH GENERATOR] Frontier:", frontier)

		while frontier != []:
			self.log("[PATH GENERATOR] Beginning iteration...")

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

			self.log("[PATH GENERATOR] Frontier:", frontier)
			self.log(f"Display:\n{str(self)}", indentation=1)

		self.log("[PATH GENERATOR] Node map:", self.node_map)

		self.goal_spreader()

		timer_end = time()
		self.log("[PATH GENERATOR] Generation time:", f"{(timer_end - timer_start):.5f}s.")
		self.log(f"Display:\n{str(self)}", indentation=1)


	@staticmethod
	def manhattan(node_1: Node, node_2: Node) -> int:
		return abs(node_1.X - node_2.X) + abs(node_1.Y - node_2.Y)


	def gbfs(self) -> bool:
		if self.is_explored:
			self.clear_explored_nodes()

		for node in self.node_map:
			node.weight = self.manhattan(node, self.end)

		timer_start = time()

		frontier, explored = [self.start], []

		while len(frontier) >= 1:

			self.log("[GBFS] Beginning iteration...")

			self.log(
				"[GBFS] Frontier:",
				[f"({node} :: {node.weight})" for node in frontier],
				indentation=1
			)

			node = frontier.pop()
			explored.append(node)
			node.state = 2 if node.state != -10 else -10

			self.log("[GBFS] Selected node:", node)

			self.log(f"Display:\n{str(self)}", indentation=1)

			candidates = [node for node in self.next_nodes(node) if node.state in (1, 10)]

			if any(candidate.coordinates == self.end.coordinates for candidate in candidates):
				self.log("[GBFS] End node:", self.end)
				timer_end = time()
				self.log("[GBFS] Search time:", f"{(timer_end - timer_start):.5f}s.")
				self.is_explored = True

				return True

			self.log("[GBFS] Candidates:", candidates, indentation=1)

			self.log(
				"[GBFS] Weight list:",
				[f"({node} :: {node.weight})" for node in candidates],
				indentation=1
			)

			frontier.extend(candidates)
			frontier = sorted(frontier, reverse=True, key=lambda x: x.weight)

		self.log("[GBFS] End node:", self.end)

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

	def __repr__(self):
		return f"({self.X}x{self.Y}) {self.__class__} instance"

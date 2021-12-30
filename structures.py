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
		-10: (82, 84, 169),
		0: (0, 0, 0),
		1: (200, 200, 200),
		2: (0, 0, 0),
		3: (182, 56, 129),
		10: (80, 210, 110)
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

	def set_state(self, state: int) -> None:
		"""Changes node's state and its linked attributes."""
		self.state = state
		self.color = self.STATE_COLOR[self.state]
		self.ascii = self.STATE_ASCII[self.state]

	def set_color(self, rgb: tuple[int, int, int]) -> None:
		"""Changes node's color."""
		self.color = rgb

	def __repr__(self):
		return f"Node(X: {self.x}, Y: {self.y}, " \
		+ f"S: {self.STATE_STRING[self.state]:10s}, W: {self.weight})"

# OLD FRONTIER
class Frontier:
	"""Data structure that contains nodes."""
	def __init__(self, initial_node: Node):
		self.nodes = [initial_node]

	def add_node(self, node: Node) -> None:
		self.nodes.append(node)

	def add_nodes(self, nodes: list[Node]) -> None:
		self.nodes.extend(nodes)

	def is_empty(self) -> bool:
		return len(self.nodes) == 0

	def contains_state(self, state: int) -> bool:
		return any(node.state == state for node in self.nodes)

	def contains_node(self, node) -> bool:
		return node in self.nodes

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

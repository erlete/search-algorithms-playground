"""Container module for the frontier classes.

This module contains three classes, one of them is a generic Frontier
interface and the others are specific to a stack or queue data structure.

Author:
-------
 - Paulo Sánchez (@erlete)
"""


from utils.node import Node


class Frontier:
    """Data structure that contains nodes."""

    def __init__(self, initial_node: Node):
        self.nodes = [initial_node]

    def add_nodes(self, nodes: list) -> None:
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

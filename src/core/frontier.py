"""Container module for the Frontier classes.

This module contains three classes: one of them is a generic Frontier
interface and the others are specific to a stack or queue data structure.

Authors:
    Paulo Sanchez (@erlete)
"""


from .node import Node


class Frontier:
    """Node container data structure.

    Contains basic methods that allow node addition and empty frontier
    checking.

    Attributes:
        nodes (list[Node]): list of contained nodes.
    """

    __slots__ = ("_nodes",)

    def __init__(self) -> None:
        """Initialize a Frontier instance."""
        self._nodes: list[Node] = []

    @property
    def nodes(self) -> list[Node]:
        """Get the nodes of the frontier.

        Returns:
            list[Node]: list of nodes of the frontier.
        """
        return self._nodes

    def add(self, value: Node | list[Node]) -> None:
        """Add a node or set of nodes to the frontier.

        Args:
            value (Node | List[Node]): node or list of nodes.

        Raises:
            TypeError: if any of the values is not a type Node.
        """
        if isinstance(value, Node):
            self._nodes.append(value)

        elif isinstance(value, (list, tuple, set)):
            self._nodes.extend(value)

        else:
            raise TypeError("Invalid type for node addition.")

    def is_empty(self) -> bool:
        """Determine whether the frontier is empty.

        Returns:
            bool: whether the frontier is empty.
        """
        return len(self._nodes) == 0

    def __str__(self) -> str:
        """Complete representation of the Frontier.

        Returns:
            str: complete representation of the Frontier.
        """
        return f"<Frontier object with {len(self._nodes)} nodes>"

    def __repr__(self) -> str:
        """Short representation of the Frontier.

        Returns:
            str: short representation of the Frontier.
        """
        return f"Frontier({self._nodes})"


class StackFrontier(Frontier):
    """Frontier variant that allows node removal in a LIFO manner."""

    def remove(self) -> Node:
        """Remove a node from the frontier.

        Returns:
            Node: the extracted node.
        """
        return self._nodes.pop()


class QueueFrontier(Frontier):
    """Frontier variant that allows node removal in a FIFO manner."""

    def remove(self) -> Node:
        """Remove a node from the frontier.

        Returns:
            Node: the extracted node.
        """
        return self._nodes.pop(0)

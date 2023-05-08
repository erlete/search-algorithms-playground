"""Container module for the Frontier classes.

This module contains three classes: one of them is a generic Frontier
interface and the others are specific to a stack or queue data structure.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


from utils.internal.node import Node


class Frontier:
    """Generic data structure that serves as node container.

    Contains basic methods that allow node addition and empty frontier
    checking.
    """

    @property
    def nodes(self):
        return self._nodes

    def __init__(self):
        self._nodes = []

    def add(self, value) -> None:
        """Adds a node to the frontier.

        Supports single or collective addition of nodes.
        """

        if isinstance(value, Node):
            self._nodes.append(value)

        elif isinstance(value, (list, tuple, set)):
            self._nodes.extend(value)

        else:
            raise TypeError("Invalid type for node addition.")

    def is_empty(self) -> bool:
        """Determines whether the frontier is empty or not."""

        return len(self._nodes) == 0

    def __str__(self):
        return f"<Frontier object with {len(self._nodes)} nodes>"

    def __repr__(self):
        return f"Frontier({self._nodes})"


class StackFrontier(Frontier):
    """Frontier variant that allows node removal in a LIFO manner."""

    def remove(self) -> None:
        """Removes a node from the frontier."""

        return self._nodes.pop()


class QueueFrontier(Frontier):
    """Frontier variant that allows node removal in a FIFO manner."""

    def remove(self) -> None:
        """Removes a node from the frontier."""

        return self._nodes.pop(0)

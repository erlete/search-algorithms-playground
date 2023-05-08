"""Container module for the Node class.

This module contains the class structure that allows node identification and
state management.

Authors:
    Paulo Sanchez (@erlete)
"""

from __future__ import annotations


class Node:
    """Data structure that represents a special element of an array.

    Each node has special properties that determine its location in the array,
    state, search weight, parent node and color.

    Attributes:
        x (int): x coordinate of the node.
        y (int): y coordinate of the node.
        state (int): state code of the node.
        parent (Node | None): parent of the node.
        weight (float): weight of the node.
        color (tuple[int, int, int]): color code of the node.
        ascii (str): ASCII representation of the node.
    """

    STATE_STRING: dict[int, str] = {
        -10: "Start",
        0: "Wall",
        1: "Path",
        2: "Explored",
        3: "Optimal",
        10: "End"
    }

    STATE_ASCII: dict[int, str] = {
        -10: 'A ',
        0: '█ ',
        1: '  ',
        2: '░ ',
        3: 'o ',
        10: 'B '
    }

    STATE_COLOR: dict[int, tuple[int, int, int]] = {
        -10: (166, 47, 47),
        0: (0, 0, 0),
        1: (169, 159, 159),
        2: (0, 0, 0),
        3: (235, 167, 89),
        10: (48, 19, 92)
    }

    def __init__(self, x: int, y: int, state: int = 0, weight: float = 0):
        """Initialize a Node instance.

        Args:
            x (int): x coordinate of the node.
            y (int): y coordinate of the node.
            state (int, optional): state code of the node. Defaults to 0.
            weight (float, optional): weight of the node. Defaults to 0.
        """
        # Node localization:
        self._x: int = x
        self._y: int = y
        self._parent: Node | None = None

        # Node classification:
        self._state: int = state
        self._weight: float = weight

        # Display:
        self._color: tuple[int, int, int] = self.STATE_COLOR[self.state]
        self._ascii: str = self.STATE_ASCII[self.state]

    @property
    def x(self) -> int:
        """Get the x coordinate of the node.

        Returns:
            int: x coordinate of the node.
        """
        return self._x

    @property
    def y(self) -> int:
        """Get the y coordinate of the node.

        Returns:
            int: y coordinate of the node.
        """
        return self._y

    @property
    def parent(self) -> Node | None:
        """Get the parent of the node, if existent.

        Returns:
            Node (optional): parent of the node, if existent.
        """
        return self._parent

    @parent.setter
    def parent(self, value: Node) -> None:
        """Set the parent of the node.

        Args:
            value (Node): parent of the node.

        Raises:
            TypeError: if the value is not a Node instance.
        """
        if not isinstance(value, Node):
            raise TypeError("Invalid type for parent assignment.")

        self._parent = value

    @property
    def state(self) -> int:
        """Get the state code of the node.

        Returns:
            int: state code of the node.
        """
        return self._state

    @property
    def weight(self) -> float:
        """Get the weight of the node.

        Returns:
            float: weight of the node.
        """
        return self._weight

    @weight.setter
    def weight(self, value: float | float) -> None:
        """Get the weight of the node.

        Args:
            value (float): weight of the node.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Invalid type for weight assignment.")

        self._weight = float(value)

    @property
    def color(self) -> tuple[int, int, int]:
        """Get the color code of the node.

        Returns:
            tuple[int, int, int]: color code of the node.
        """
        return self._color

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        """Set the color code of the node.

        Args:
            value (tuple[int, int, int]): color code of the node.

        Raises:
            TypeError: if the value is not a tuple of integers.
            TypeError: if any item of the value is not an integer.
            ValueError: if the length of the tuple is not 3.
        """
        if not isinstance(value, tuple):
            raise TypeError("value must be a tuple of integers.")

        if not all(isinstance(item, int) for item in value):
            raise TypeError("all elements of value must be integers.")

        if len(value) != 3:
            raise ValueError("value must have 3 elements.")

        self._color = value

    @property
    def ascii(self) -> str:
        """Get the ASCII character of the node.

        Returns:
            str: ASCII character of the node.
        """
        return self._ascii

    def set_state(
        self,
        state: int,
        set_color: bool = True,
        set_ascii: bool = True
    ) -> None:
        """Change node state and linked attributes.

        Args:
            state (int): new state value.
            set_color (bool): whether the node's color should be updated.
            set_ascii (bool): whether the node's ASCII representation should
                be updated.
        """
        self._state = state

        if set_color:
            self._color = self.STATE_COLOR[self.state]
        if set_ascii:
            self._ascii = self.STATE_ASCII[self.state]

    def __str__(self) -> str:
        """Complete representation of the Frontier.

        Returns:
            str: complete representation of the Frontier.
        """
        return f"""Node(
    X: {self._x},
    Y: {self._y},
    State: {self.STATE_STRING[self._state]},
    Weight: {self._weight},
    Parent: {self._parent}
)"""

    def __repr__(self) -> str:
        """Short representation of the Frontier.

        Returns:
            str: short representation of the Frontier.
        """
        return f"<Node object with state {self._state}>"

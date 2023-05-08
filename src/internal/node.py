"""Container module for the Node class.

This module contains the class structure that allows node identification and
state management.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


class NodeBase:
    """Represents the basic attributes and methods of a Node class.

    Contains relational dictionaries for state, ascii and color representation
    of the node. Also contains all node attributes' getters and setters.
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
        1: (169, 159, 159),
        2: (0, 0, 0),
        3: (235, 167, 89),
        10: (48, 19, 92)
    }

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if not isinstance(value, Node):
            raise TypeError("Invalid type for parent assignment.")

        self._parent = value

    @property
    def state(self):
        return self._state

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Invalid type for weight assignment.")

        self._weight = value

    @property
    def color(self):
        return self._color

    @property
    def ascii(self):
        return self._ascii


class Node(NodeBase):
    """Data structure that represents a special element of an array.

    Each node has special properties that determine its location in the array,
    state, search weight, parent node and color.

    Parameters
    ----------
     - x : int
        X axis coordinate (matrix row).
     - y : int
        Y axis coordinate (matrix column).
     - state : int
        Value that defines the node's qualities (0: wall, 1: path...).
     - weight : int
        Value that measures how much the overall path cost increases when the
        node is considered as part of it.
    """

    def __init__(self, x: int, y: int, state=0, weight=0):
        # Node localization:
        self._x, self._y = x, y
        self._parent = None

        # Node classification:
        self._state = state
        self._weight = weight

        # Display:
        self._color = self.STATE_COLOR[self.state]
        self._ascii = self.STATE_ASCII[self.state]

    def set_state(self, state: int, set_color=True, set_ascii=True) -> None:
        """Changes state and its linked attributes.

        Parameters:
        -----------
         - state : int
            New state value.
         - set_color : bool
            Determines whether the node's color should be updated or not.
         - set_ascii : bool
            Determines whether the node's ASCII representation should be
            updated or not.
        """

        self._state = state

        if set_color:
            self._color = self.STATE_COLOR[self.state]
        if set_ascii:
            self._ascii = self.STATE_ASCII[self.state]

    def set_color(self, rgb: tuple) -> None:
        """Changes node color."""

        self._color = rgb

    def set_parent(self, parent):
        """Changes parent node reference."""

        self._parent = parent

    def __str__(self):
        return f"<Node object with state {self._state}>"

    def __repr__(self):
        return f"""Node(
    X: {self._x},
    Y: {self._y},
    State: {self.STATE_STRING[self._state]},
    Weight: {self._weight},
    Parent: {self._parent}
)"""

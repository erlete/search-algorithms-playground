class Node:
    """Data structure that represents an element of an array with special
    properties that determine its location in the array, its state, weight,
    parent node, color...

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

    def __init__(self, x: int, y: int, *, state=0, weight=0):
        # Node localization:
        self.x, self.y = x, y
        self.parent = None

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

    def set_color(self, rgb: tuple) -> None:
        """Changes node's color."""
        self.color = rgb

    def set_parent(self, parent):
        """Changes node's parent node."""
        self.parent = parent

    def __repr__(self):
        return f"Node(X: {self.x}, Y: {self.y}, " \
            + f"S: {self.STATE_STRING[self.state]:10s}, W: {self.weight})"

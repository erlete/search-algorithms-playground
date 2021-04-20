from random import randint
from sys import path

class Maze:

    def __init__(self):
        with open(path[0] + "/textual_log.txt", 'w') as f:  # Resets the textual log file
            f.write('\n')
        with open(path[0] + "/visual_log.txt", 'w') as f:   # Resets the visual log file
            f.write('\n')

    def uniqueappend(self, element, group):
        """
        Method used to append unique items only. Prevents confusing 'if-else' statements reiteration.
        """
        if element not in group:
            group.append(element)

    def display(self):
        """
        Display method for 'Base' property. Produces a symbolic representation from the numerical array.
        """
        for row in self.Base:
            printed_row = ''
            for element in row:
                if element == -1:
                    printed_row += '# ' # Outer wall display
                elif element == 0:
                    printed_row += '█ ' # Inner wall display
                elif element == 1:
                    printed_row += '  ' # Generated path display
                elif element == 2:
                    printed_row += 'x ' # Explored path display
                elif element == 'A':
                    printed_row += 'A ' # Initial state display
                elif element == 'B':
                    printed_row += 'B ' # Goal state display
            print(printed_row)

    def log(self, item: str, switch = True):
        """
        Logging method for debugging markers in the algorithm.
        """
        if switch == True:
            with open(path[0] + "/textual_log.txt", 'a') as f:
                f.write(item + '\n')

    def logdisplay(self, switch = True):
        """
        Logging method for 'Base' property. Same behavior as the 'display' method.
        """
        if switch == True:
            with open(path[0] + "/visual_log.txt", 'a') as f:
                for row in self.Base:
                    printed_row = ''
                    for element in row:
                        if element == -1:
                            printed_row += '# ' # outer wall
                        elif element == 0:
                            printed_row += '█ ' # inner wall
                        elif element == 1:
                            printed_row += '  ' # path
                        elif element == 2:
                            printed_row += '+ ' # explored path
                        elif element == 'A':
                            printed_row += 'A ' # initial state
                        elif element == 'B':
                            printed_row += 'B ' # goal state
                    f.write(printed_row + '\n')
                f.write('\n\n')

                for row in self.Base:
                    f.write(str(row)[1:-1].replace(',', ''))
                f.write('\n\n')

    def basegenerator(self, dimensions = 10): # review (remove outer borders) (check for surrounding and sqsurrounding nodes behavior)
        """
        Generates a numerical array, given its code structure (-1 = outer wall; 0 = inner wall; 1 = path; 'A' = initial state).

        The 'dimensions' parameter can be set in a regular or irregular way, using either an 'int' or a 'tuple' datatype.
        """
        # Error Prevention
        if type(dimensions) == int:
            dimensions = (dimensions, dimensions)
        elif type(dimensions) == tuple and len(dimensions) == 2:
            for value in dimensions:
                if value <= 0:
                    raise Exception("Negative values cannot be used to set the array dimensions")
        else:
            raise Exception("The array dimensions must be specified either as an 'int' or two-term 'tuple'")

        self.Base = [[0 for i in range(dimensions[0] + 2)] for j in range(dimensions[1] + 2)] # base generation (inner and outer walls only)

        self.Base[0] = [-1 for i in range(len(self.Base[0]))]   # top outer wall
        for i in range(len(self.Base)):
                self.Base[i][0] = -1                            # left outer wall
                self.Base[i][-1] = -1                           # right outer wall
        self.Base[-1] = [-1 for i in range(len(self.Base[0]))]  # bottom outer wall

        self.Base[1][1] = 'A' # initial state
        self.Initial_position = (1, 1)

    def nextnodes(self, coordinates):
        """
        Gets the nodes next to the given coordinates (top, right, bottom and left).

        The order in which the surrounding nodes are passed to the algorithm is set randomly, to prevent data pre-setting.
        """
        # Generates an order array:
        order = []
        while True:
            value = randint(0, 3)
            self.uniqueappend(value, order)
            if len(order) == 4:
                break

        # Gets the nodes surrounding the one specified:
        surrounding_nodes = []
        for node in [
                (coordinates[0] - 1, coordinates[1]),   # top
                (coordinates[0], coordinates[1] + 1),   # right
                (coordinates[0] + 1, coordinates[1]),   # bottom
                (coordinates[0], coordinates[1] - 1)    # left
                ]:
            try:
                surrounding_nodes.append(node)
            except IndexError:
                pass

        # Outputs the surrounding nodes in the randomly defined order:
        output = []
        while True:
            for value in order:
                self.uniqueappend(surrounding_nodes[value], output)
            if len(output) == 4:
                break

        return output

    def surroundings(self, coordinates):
        """
        Gets the values in the square surroundings of the given coordinates. This method is used in order to prevent path mixing during its generation.
        """
        surrounding_nodes = []
        for node in [
            (coordinates[0] - 1, coordinates[1] - 1),   # top left
            (coordinates[0] - 1, coordinates[1]),       # top center
            (coordinates[0] - 1, coordinates[1] + 1),   # top right
            (coordinates[0], coordinates[1] - 1),       # left
            (coordinates[0], coordinates[1] + 1),       # right
            (coordinates[0] + 1, coordinates[1] - 1),   # bottom left
            (coordinates[0] + 1, coordinates[1]),       # bottom center
            (coordinates[0] + 1, coordinates[1] + 1)    # bottom right
            ]:
            try:
                surrounding_nodes.append(node)
            except IndexError:
                pass
        return surrounding_nodes

    def distance(self, item_1: tuple, item_2: tuple): # deprecated, fix abs() # review
        """
        Returns the diagonal distance between two nodes.
        """
        return format(((item_2[0] - item_1[0]) ** 2 + (item_2[1] - item_1[1]) ** 2) ** (1 / 2), '.4f')

    def manhattan(self, item_1: tuple, item_2: tuple):
        """
        Returns the manhattan (square) distance between two nodes.
        """
        return (abs(item_2[0]) - abs(item_1[0])) + (abs(item_2[1]) - abs(item_1[1]))

    def wdistance(self, item: tuple): # review
        """
        Returns the weighted manhattan (square) distance between two nodes.
        """
        return (
            (self.Goal_position[0] - item[0]) + (self.Goal_position[1] - item[1])
            ), (
                (item[0] - self.Initial_position[0]) + (item[1] - self.Initial_position[1])
                )

    def caesar(self, paths, spread_index):
        """
        Random path divergence generator. Takes one or multiple path divergence possibilities and selects some of them.

        The 'spread_index' sets the probability of path selection ( = 0: no paths are skipped; = 10: all paths are skipped). Note that values near 10 might generate an endless loop.

        The name is due to the 'lives, dies' choice of Julius Caesar during collosseum games. # review
        """
        # Error Prevention:
        if len(paths) == 0:
            return None
        elif spread_index >= 10:
            raise Exception("Values over 10 for 'spread_index' generate an endless loop.")

        else:
            selected = []
            while True:
                for element in paths:
                    selection_value = randint(0, 10)
                    if selection_value >= spread_index:
                        selected.append(element)
                if len(selected) >= 1:
                    return selected

    def goalspreader(self, nodes_changed):
        """
        Sets the position of the goal state at the farthest coordinate possible in the array.
        """
        for i in range(len(self.Base)):
            for j in range(len(self.Base[i])):
                if self.Base[i][j] == 'A':
                    initial_position = (i, j)

        total = (initial_position[0] + nodes_changed[0][0], initial_position[1] + nodes_changed[0][1])

        for i in range(len(nodes_changed)):
            if (initial_position[0] + nodes_changed[i][0], initial_position[1] + nodes_changed[i][1]) > total:
                total = (initial_position[0] + nodes_changed[i][0], initial_position[1] + nodes_changed[i][1])

        return (total[0] - initial_position[0], total[1] - initial_position[1])

    def pathgenerator(self, iterations = 200, spread_index = 3):
        """
        Randomly generates a pathway for the array.

        The 'iterations' parameter determines after how many path node generation attemps the algorithm should stop. For low values, the path might have a short length.
        """
        self.Frontier = []
        self.Nodes_in_range = []
        self.Coordinates = [self.Initial_position]
        self.Nodes_changed = self.Coordinates.copy()

        for iteration_count in range(iterations):
            for coordinate in self.Coordinates:
                for candidate_in_range in self.nextnodes(coordinate):
                    if self.Base[candidate_in_range[0]][candidate_in_range[1]] in [-1, 'A', 1]:
                        continue
                    self.uniqueappend(candidate_in_range, self.Nodes_in_range)

            for candidate in self.Nodes_in_range:
                can_make_path = True
                nearby_path = 0
                for check in self.surroundings(candidate):
                    if self.Base[check[0]][check[1]] in [1, 'A']:
                        nearby_path += 1

                        if nearby_path == 3:
                            can_make_path = False

                if can_make_path == True:
                    self.Frontier.append(candidate)

            self.Frontier = self.caesar(self.Frontier, spread_index)
            if self.Frontier == None or iteration_count == iterations:
                self.Goal_position = self.goalspreader(self.Nodes_changed)
                self.Base[self.Goal_position[0]][self.Goal_position[1]] = 'B'
                return None
            else:
                for i in self.Frontier:
                    self.uniqueappend(i, self.Nodes_changed)
            self.Coordinates = []
            for i in self.Frontier:
                self.Base[i[0]][i[1]] = 1
                self.Coordinates.append(i)
            self.Nodes_in_range = []
            self.Frontier = []

    def quickgen(self, dimensions = 10, iterations = 200, spread_index = 3):
        """
        Quick array and path generation with result display.
        """
        self.basegenerator(dimensions)
        self.pathgenerator(iterations, spread_index)
        self.display()

maze = Maze()
maze.basegenerator(10)
maze.pathgenerator()
maze.display()

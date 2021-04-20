from random import randint
from sys import path

class Maze:
    """
    This class generates a blank array of (n x m) dimensions, composed by '-1' values in the borders and '0' values in the middle, the 'Base' property.

    Given that array, an algorithm generates a 'path', made out of '1' values, which later on can be evaluated by a search algorithm to keep track of the explored path, whose value is '2'.

    There are some debugging methods, such as 'log' and 'logdisplay', that are used in order to properly comprehend the path generation and solving behavior, and also help prevent potential bugs.
    """
    # Tool method

    def uniqueappend(self, element, group):
        """
        Method used to append unique items only. Prevents confusing 'if-else' statements reiteration.
        """
        if element not in group:
            group.append(element)

    # Visualization method

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

    # Debugging methods

    def log(self, item: str, switch = False):
        """
        Logging method for convenient data markers in the algorithm.
        """
        if switch == True:
            try:
                f = open(path[0] + "/textual_log.txt", 'r')
            except FileNotFoundError:
                f = open(path[0] + "/textual_log.txt", 'a')
                f.write(item + '\n')
                f.close()

    def logdisplay(self, switch = False):
        """
        Logging method for 'Base' property. Same behavior as the 'display' method.
        """
        if switch == True:
            try:
                f = open(path[0] + "/visual_log.txt", 'r')
            except FileNotFoundError:
                f = open(path[0] + "/visual_log.txt", 'a')
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

                f.close()

    # Base generation method

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
                    raise Exception("Negative values cannot be used to set the array dimensions.")
                elif value > 2:
                    raise Exception("The array can only be bidimensional.")
        else:
            raise Exception("The array dimensions must be specified either as an 'int' or two-term 'tuple'.")

        # Base generation
        self.Base = [[0 for i in range(dimensions[0] + 2)] for j in range(dimensions[1] + 2)] # Base generation (0)

        self.Base[0] = [-1 for i in range(len(self.Base[0]))]   # Top outer wall (-1)
        self.Base[-1] = self.Base[0].copy()                     # Bottom outer wall (-1)
        for i in range(len(self.Base)):
                self.Base[i][-1] = -1                           # Right outer wall (-1)
                self.Base[i][0] = -1                            # Left outer wall (-1)

        self.Base[1][1] = 'A'           # Initial state definition
        self.Initial_position = (1, 1)  # Initial state position

    # Node surroundings evaluation methods

    def nextnodes(self, coordinates):
        """
        Gets the nodes next to the given coordinates (top, right, bottom and left slots).

        The order in which the surrounding nodes are passed to the algorithm is set randomly, to prevent data pre-setting.
        This is done by getting the coordinates of the nodes surrounding the one specified and appending those coordinates to an output array in a randomly defined order.

        Note: there must be a more efficient alternative to this process, however, this is not a priority just yet.
        """
        # Process illustration:

            #       T
            #   L   C   R
            #       B

        # Gets the nodes surrounding the one specified
        surrounding_nodes = []
        for node in [
                (coordinates[0] - 1, coordinates[1]),   # Top
                (coordinates[0], coordinates[1] + 1),   # Right
                (coordinates[0] + 1, coordinates[1]),   # Bottom
                (coordinates[0], coordinates[1] - 1)    # Left
                ]:
            surrounding_nodes.append(node)

        # Generates an order array
        order = []
        while True: # The infinite loop is necessary in order to provide with unique, random index appending to the 'order' array
            value = randint(0, len(surrounding_nodes) - 1)
            self.uniqueappend(value, order) # If a value is repeated, it does not get appended
            if len(order) == len(surrounding_nodes):
                break

        # Outputs the surrounding nodes in the randomly defined order
        output = []
        for value in order:
            self.uniqueappend(surrounding_nodes[value], output)

        return output

    def surroundings(self, coordinates):
        """
        Gets the values in the square surroundings of the given coordinates. This method is used in order to prevent path mixing during its generation.

        Since the method is only used to evaluate the amount of nearby 'path' values (1) near the considered node during path generation, there is no point in setting up a random order method.
        """
        # Process illustration:

            #   TL  TC  TR
            #   ML  CC  MR
            #   BL  BC  BR

        # Gets the nodes surrounding the one specified
        surrounding_nodes = []
        for node in [
            (coordinates[0] - 1, coordinates[1] - 1),   # Top left
            (coordinates[0] - 1, coordinates[1]),       # Top center
            (coordinates[0] - 1, coordinates[1] + 1),   # Top right
            (coordinates[0], coordinates[1] + 1),       # Middle right
            (coordinates[0] + 1, coordinates[1] + 1),   # Bottom right
            (coordinates[0] + 1, coordinates[1]),       # Bottom center
            (coordinates[0] + 1, coordinates[1] - 1),   # Bottom left
            (coordinates[0], coordinates[1] - 1)       # Middle left
            ]:
            surrounding_nodes.append(node)

        return surrounding_nodes

    def caesar(self, paths, spread_index):
        """
        Random path divergence generator. Takes one or multiple path divergence possibilities and selects at least one of them.

        The 'spread_index' sets the probability of path selection ( = 0: all possible paths are selected; = 10: all possible paths are skipped).
        Note that values near 10 might generate an endless loop. Also, negative values act the same way as zero.

        The name is due to the 'lives, dies' choice of Julius Caesar during colosseum gladiator games.
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
        # Sets a default higher distance
        higher_distance = (self.Initial_position[0] + nodes_changed[0][0], self.Initial_position[1] + nodes_changed[0][1])

        # Checks every path node's distance to origin to determine which one is the farthest one
        for node in nodes_changed:
            if (self.Initial_position[0] + node[0], self.Initial_position[1] + node[1]) >= higher_distance:
                higher_distance = (self.Initial_position[0] + node[0], self.Initial_position[1] + node[1])

        return (higher_distance[0] - self.Initial_position[0], higher_distance[1] - self.Initial_position[1])

    # Path generation method

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
                    elif self.Base[candidate_in_range[0]][candidate_in_range[1]] == 'B':
                        keep = False
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

    # Miscellaneous

    def quickgen(self, dimensions = 10, iterations = 200, spread_index = 3):
        """
        Quick array and path generation with result display.
        """
        self.basegenerator(dimensions)
        self.pathgenerator(iterations, spread_index)
        self.display()

maze = Maze()
maze.basegenerator()
maze.pathgenerator()
maze.display()
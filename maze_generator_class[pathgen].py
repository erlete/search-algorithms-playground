from random import randint  # random value generation
from sys import path        # data export path
from time import time       # time benchmarking

class Maze:
    """
    This class generates a blank array of (n x m) dimensions, made of '0' values, passed to the 'Base' property.

    Given that array, an algorithm generates a 'path', made out of '1' values, which later on can be evaluated by a search algorithm to keep track of the explored path, whose value is '2'.

    There are some debugging methods, such as 'log' and 'logdisplay', that are used in order to properly comprehend the path generation and solving behavior, and also help prevent potential bugs.
    """
    # Visualization method

    def display(self):
        """
        Display method for 'Base' property. Produces a symbolic representation from the numerical array.
        """
        printed_row = '# ' + '— ' * self.Dimensions[0] + '#'
        print(printed_row)
        for row in self.Base:
            printed_row = '| '
            for element in row:
                if element == 0:
                    printed_row += '█ ' # Inner wall display
                elif element == 1:
                    printed_row += '  ' # Generated path display
                elif element == 2:
                    printed_row += 'x ' # Explored path display
                elif element == -10:
                    printed_row += 'A ' # Initial state display
                elif element == 10:
                    printed_row += 'B ' # Goal state display
            printed_row += '| '
            print(printed_row)
        printed_row = '# ' + '— ' * self.Dimensions[0] + '#'
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
                        if element == 0:
                            printed_row += '█ ' # inner wall
                        elif element == 1:
                            printed_row += '  ' # path
                        elif element == 2:
                            printed_row += '+ ' # explored path
                        elif element == -10:
                            printed_row += 'A ' # initial state
                        elif element == 10:
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
        Generates a numerical array, given its code structure (0 = inner wall; 1 = path; -10 = initial state).

        The 'dimensions' parameter can be set in a regular or irregular way, using either an 'int' or a 'tuple' datatype.
        """
        # Error Prevention
        if type(dimensions) == int:
            dimensions = (dimensions, dimensions)
        elif type(dimensions) == tuple and len(dimensions) == 2:
            for value in dimensions:
                if value <= 0:
                    raise Exception("Negative values cannot be used to set the array dimensions.")
        elif type(dimensions) == tuple and len(dimensions) != 2:
            raise Exception("The array can only be bidimensional.")
        else:
            raise Exception("The array dimensions must be specified either as an 'int' or two-term 'tuple'.")
        self.Dimensions = dimensions # Class-wide variable for comparison

        # Base generation
        self.Base = [[0 for i in range(dimensions[1])] for j in range(dimensions[0])] # Base generation (0)

        self.Base[0][0] = -10           # Initial state definition
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
            if node[0] <= self.Dimensions[0] - 1 and node[1] <= self.Dimensions[1] - 1:
                if node[0] >= 0 and node[1] >= 0:
                    surrounding_nodes.append(node)
            #surrounding_nodes.append(node) if node[0] >= 0 and node[1] >= 0 and node <= self.Dimensions else None

        # Generates an order array
        order = []
        while True: # The infinite loop is necessary in order to provide with unique, random index appending to the 'order' array
            value = randint(0, len(surrounding_nodes) - 1)
            order.append(value) if value not in order else None
            if len(order) == len(surrounding_nodes):
                break

        # Outputs the surrounding nodes in the randomly defined order
        output = []
        for value in order:
            output.append(surrounding_nodes[value]) if surrounding_nodes[value] not in output else None
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
            if node[0] <= self.Dimensions[0] - 1 and node[1] <= self.Dimensions[1] - 1:
                if node[0] >= 0 and node[1] >= 0:
                    surrounding_nodes.append(node)
            #surrounding_nodes.append(node) if node[0] > 0 and node[1] > 0 and node else None
        return surrounding_nodes

    def caesar(self, paths):
        """
        Random path divergence generator. Takes one or multiple path divergence possibilities and selects at least one of them.

        The name is due to the 'lives, dies' choice of Julius Caesar during colosseum gladiator games.
        """
        # Error Prevention:
        if len(paths) == 0:
            return []

        while True:
            selected = []
            for element in paths:
                value = randint(0, 1)
                selected.append(element) if value else None
            if len(selected) >= 1:
                break

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

    def pathgenerator(self):
        """
        Randomly generates a pathway for the array.

        The 'iterations' parameter determines after how many path node generation attemps the algorithm should stop. For low values, the path might have a short length.
        """

        d = 1

        self.Frontier = [self.Initial_position]
        print('Generating array...')
        ts = time()

        while True:
            selected_nodes, candidates = [], []

            # Checks for nodes around the specified one that are not "path tiles" (1) or the initial node (-10)
            for coordinates in self.Frontier:
                for neighbor in self.nextnodes(coordinates):
                    if self.Base[neighbor[0]][neighbor[1]] not in [1, -10]:
                        candidates.append(neighbor) if neighbor not in candidates else None
            
            # The nodes that were able to be transformed into 'path' are set as candidates and evaluated regardind the surrounding path tiles
            for candidate in candidates:
                can_make_path = True
                nearby_path_tiles = 0
                for coordinates in self.surroundings(candidate):
                    if self.Base[coordinates[0]][coordinates[1]] in [1, -10]:
                        nearby_path_tiles += 1
                        if nearby_path_tiles == 3:
                            can_make_path = False
                            break
                if can_make_path == True:
                    selected_nodes.append(candidate) # Appends the valid nodes to the 'selected' list

            # Out of the 'selected' nodes array, a random amount of divergent paths are generated
            selected_nodes = self.caesar(selected_nodes)

            # End of the path generation check
            if selected_nodes == []: # If the generation process has finished (there are no avaliable nodes for path-making)
                self.Goal_position = self.goalspreader(self.Frontier)
                self.Base[self.Goal_position[0]][self.Goal_position[1]] = 10
                te = time()
                print(f"Array generated correctly. Time elapsed: {format(te - ts, '.4f')}s")
                return 1
            else: # If the generation process has not yet finished (there are avaliable nodes for path-making)
                for coordinates in selected_nodes:
                    self.Base[coordinates[0]][coordinates[1]] = 1 # Sets the selected nodes as path tiles (1)
                    self.Frontier.append(coordinates) if coordinates not in self.Frontier else None # Appends the nodes to the 'Frontier' array

maze = Maze()
maze.basegenerator(20)
maze.pathgenerator()
maze.display()

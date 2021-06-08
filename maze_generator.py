from random import randint  # random value generation
from time import time       # time benchmarking

class Maze:
    """
    This class generates a blank array of (m x n) dimensions, made of '0' values, passed to the 'Base' property.

    Given that array, an algorithm generates a 'path', made out of '1' values, which later on can be evaluated by a search algorithm to keep track of the explored path, whose value is '2'.

    The initial and goal states are represented by '-10' and '10' values, respectively.
    """
    # Base generation method

    def basegenerator(self, dimensions = 10): # review (remove outer borders) (check for surrounding and sqsurrounding nodes behavior)
        """
        Generates a numerical array, given its code structure (0 = inner wall; 1 = path; -10 = initial state).

        The 'dimensions' parameter can be set in a regular or irregular way, using either an 'int' or a 'tuple' datatype.
        """
        # Error Prevention
        if type(dimensions) == int:
            dimensions = (dimensions, dimensions)
        elif type(dimensions) == tuple:
            if len(dimensions) == 2:
                for value in dimensions:
                    if value <= 1:
                        raise Exception("Negative, '0' and '1' values cannot be used to set the array dimensions.")
            elif len(dimensions) != 2:
                raise Exception("The array can only be bidimensional.")
        else:
            raise Exception("The array dimensions must be specified either as an 'int' greater than '1' or a two-term 'tuple'.")

        # Base generation
        self.Dimensions = dimensions
        self.Base = [[0 for i in range(dimensions[1])] for j in range(dimensions[0])] # Base generation (0)

        # Initial state definition
        self.Base[0][0] = -10
        self.Initial = (0, 0)

    # Node surroundings evaluation methods

    def nextnodes(self, coordinates):
        """
        Gets the nodes immediately next to the given coordinates (top, right, bottom and left slots).

        The order in which the surrounding nodes are passed to the algorithm is set in a random way, to prevent data pre-setting.
        This is done by getting the coordinates of the nodes surrounding the one specified and appending those coordinates to an output array in a randomly defined order.

        Note: there must be a more efficient alternative to this process, however, this is not a priority just yet.
        
        Process illustration:

                T
            L   X   R
                B
        """
        # Gets the nodes surrounding the one specified
        next_nodes = []
        for node in [
                (coordinates[0] - 1, coordinates[1]),   # Top
                (coordinates[0], coordinates[1] + 1),   # Right
                (coordinates[0] + 1, coordinates[1]),   # Bottom
                (coordinates[0], coordinates[1] - 1)    # Left
                ]:
            # The node is passed to the array if its coordinates are possitive (due to negative list index subscripting interference) and they are inside the dimensions range of the array
            next_nodes.append(node) if (node[0] <= self.Dimensions[0] - 1 and node[1] <= self.Dimensions[1] - 1) and (node[0] >= 0 and node[1] >= 0) else None

        # Generates a random order array
        order = []
        while True: # The infinite loop is necessary in order to provide with unique, random index appending to the 'order' array
            selector = randint(0, len(next_nodes) - 1)
            order.append(selector) if selector not in order else None
            if len(order) == len(next_nodes):
                break

        # Outputs the valid nodes in the randomly defined order
        output = []
        for value in order:
            output.append(next_nodes[value]) if next_nodes[value] not in output else None

        return output

    def surroundings(self, coordinates):
        """
        Gets the values in the square surroundings of the given coordinates. This method is used in order to prevent path mixing during its generation.

        Since the method is only used to evaluate the amount of nearby 'path' values (1) near the considered node during path generation, there is no point in setting up a random order method.
        
        Process illustration:

            TL  TC  TR
            ML  XX  MR
            BL  BC  BR
        """
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
            (coordinates[0], coordinates[1] - 1)        # Middle left
            ]:
            surrounding_nodes.append(node) if (node[0] <= self.Dimensions[0] - 1 and node[1] <= self.Dimensions[1] - 1) and (node[0] >= 0 and node[1] >= 0) else None

        return surrounding_nodes

    def caesar(self, nodes):
        """
        Random path divergence generator. Takes one or multiple path divergence possibilities and selects at least one of them.

        The name is due to the 'lives, dies' choice of Julius Caesar during colosseum gladiator games.
        """
        # Error Prevention:
        if len(nodes) == 0:
            return []

        # Randomly selects a sample from the array
        while True:
            sample = []
            for element in nodes:
                selector = randint(0, 1)
                sample.append(element) if selector else None
            if len(sample) >= 1: # Prevents forced path-generation interruption due to lack of nodes avaliable
                break

        return sample

    def goalspreader(self, path_tiles):
        """
        Sets the position of the goal state at the farthest coordinate possible in the array.
        """
        # Sets a default distance
        distance = (self.Initial[0] + path_tiles[0][0], self.Initial[1] + path_tiles[0][1])

        # Checks every path path's distance to origin to determine which one is the farthest one
        for path in path_tiles:
            if (self.Initial[0] + path[0], self.Initial[1] + path[1]) >= distance:
                distance = (self.Initial[0] + path[0], self.Initial[1] + path[1])

        return (distance[0] - self.Initial[0], distance[1] - self.Initial[1])

    # Path generation method

    def pathgenerator(self):
        """
        Randomly generates a pathway for the array.
        """
        ts = time()
        print('Generating array...')

        frontier = [self.Initial]

        while True:
            selected_nodes, candidates = [], []

            # Checks for new path candidates around the node whose values are not '1' (path) nor '-10' (initial node)
            for coordinates in frontier:
                for neighbor in self.nextnodes(coordinates):
                    if self.Base[neighbor[0]][neighbor[1]] not in [1, -10]:
                        candidates.append(neighbor) if neighbor not in candidates else None
            
            # The candidates are evaluated regardind the surrounding path tiles
            for candidate in candidates:
                can_make_path = True
                nearby_path_tiles = 0

                # Checks if there are nearby paths in the surrounding tiles
                for coordinates in self.surroundings(candidate):
                    if self.Base[coordinates[0]][coordinates[1]] in [1, -10]:
                        nearby_path_tiles += 1
                        # If there are more than two nearby paths, there could be path mixing (not cool), so the node is skipped
                        if nearby_path_tiles == 3:
                            can_make_path = False
                            break

                # Appends the valid candidates to the nodes that will be transformed into path tiles
                if can_make_path == True:
                    selected_nodes.append(candidate)

            # Out of the candidates' array, only a random sample of them is passed (prevents pre-setting of the data)
            selected_nodes = self.caesar(selected_nodes)

            # Check for the end of the path generation process
            if selected_nodes == []: # Generation process finished
                self.Goal = self.goalspreader(frontier)
                self.Base[self.Goal[0]][self.Goal[1]] = 10

                te = time()
                print(f"Array generated correctly\tTime elapsed: {format(te - ts, '.4f')}s")

                return 1
            else: # Generation process not yet finished (there are avaliable nodes for path-making)
                for coordinates in selected_nodes:
                    self.Base[coordinates[0]][coordinates[1]] = 1
                    frontier.append(coordinates) if coordinates not in frontier else None

    # Visualization method

    def display(self):
        """
        Display method for 'Base' property. Produces a symbolic representation from the numerical array.
        """
        printed_row = '╔═' + '══' * self.Dimensions[1] + '╗'
        print(printed_row)
        for row in self.Base:
            printed_row = '║ '
            for element in row:
                if element == 0:
                    printed_row += '█ ' # Inner wall display
                elif element == 1:
                    printed_row += '  ' # Generated path display
                elif element == 2:
                    printed_row += '░ ' # Explored path display
                elif element == 3:
                    printed_row += '≡ ' # Tracked path display
                elif element == -10:
                    printed_row += 'A ' # Initial state display
                elif element == 10:
                    printed_row += 'B ' # Goal state display
            printed_row += '║ '
            print(printed_row)
        printed_row = '╚═' + '══' * self.Dimensions[1] + '╝'
        print(printed_row)

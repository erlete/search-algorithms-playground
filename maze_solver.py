from maze_generator import Maze
from time import time

class Solver():

    def __init__(self, obj: object):
        self.Base, self.Dimensions = obj.Base, obj.Dimensions
        self.Initial, self.Goal = obj.Initial, obj.Goal
        self.nextnodes, self.surroundings, self.display = obj.nextnodes, obj.surroundings, obj.display

        self.Distances = dict()
        for row in range(len(self.Base)):
            for column in range(len(self.Base[row])):
                if self.Base[row][column] == 1:
                    self.Distances[(row, column)] = self.manhattan((row, column))

    def manhattan(self, coordinates: tuple):
        """
        Returns the manhattan distance between two nodes (sum of the absolute cartesian coordinates difference between a selected node and the goal node).
        The values are set as absolute to prevent search deviations due to negative coordinates addition.
        """
        return abs(self.Goal[0] - coordinates[0]) + abs(self.Goal[1] - coordinates[1])

    def log(self, item, switch):
        if switch:
            print(item)

    def solve_1(self):
        """
        Depth-First Search (DFS).
        """        
        global explored_nodes, frontier

        ts = time()
        explored = list()
        frontier = self.nextnodes(self.Initial)

        while True:

            # If there are nodes to be explored (avaliable solution)
            if len(frontier) >= 1:
                
                # 1. Node extraction from the frontier
                node = frontier[-1]
                frontier = frontier[:-1]

                # 2. Node conversion to path
                if node not in [self.Initial, self.Goal]:
                    self.Base[node[0]][node[1]] = 2
                    explored.append(node) if node not in explored else None

                    # 3. Neighbor gathering and pathfinding process termination evaluation
                    for neighbor in self.nextnodes(node):
                        if self.Base[neighbor[0]][neighbor[1]] == 1:
                            frontier.append(neighbor) if neighbor not in frontier else None
                        elif self.Base[neighbor[0]][neighbor[1]] == 10:
                            te = time()
                            print(f"Array searched correctly. Time elapsed: {format(te - ts, '.4f')}s.")
                            return 1
            
            # If there are no nodes to be explored (no solution)
            else:
                return 0

    def solve_2(self):
        """
        Greedy Best-First Search (GBFS).
        """
        global explored, frontier

        ts = time()

        frontier, explored = list(), [self.Initial]
        for node in self.nextnodes(self.Initial):
            if self.Base[node[0]][node[1]] == 1:
                frontier.append(node)

        while True:

            # If there are nodes to be explored (avaliable solution)
            if len(frontier) >= 1:

                # 1. Node extraction from the frontier
                node = frontier[-1]
                for candidate in frontier: # Takes the node with the lower distance to goal
                    if self.Distances[(candidate[0], candidate[1])] < self.Distances[(node[0], node[1])]:
                        node = candidate
                del frontier[frontier.index(node)]

                # 2. Node conversion to path
                if node not in [self.Initial, self.Goal]:
                    self.Base[node[0]][node[1]] = 2
                    explored.append(node) if node not in explored else None

                    # 3. Neighbor gathering and pathfinding process termination evaluation
                    for neighbor in self.nextnodes(node):
                        if self.Base[neighbor[0]][neighbor[1]] == 1:
                            frontier.append(neighbor) if neighbor not in frontier else None
                        elif self.Base[neighbor[0]][neighbor[1]] == 10:
                            te = time()
                            print(f"Array searched correctly. Time elapsed: {format(te - ts, '.4f')}s.")
                            return 1

            # If there are no nodes to be explored (no solution)
            else:
                return 0

maze = Maze()
maze.basegenerator((30, 60)); maze.pathgenerator(); maze.display()

solve = Solver(maze)
solve.solve_2(); solve.display()
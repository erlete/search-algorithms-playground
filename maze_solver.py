from maze_generator import Maze
from time import time

class Solver():

    def __init__(self, obj: object):
        self.Base, self.Dimensions = obj.Base, obj.Dimensions
        self.Initial, self.Goal = obj.Initial, obj.Goal
        self.nextnodes, self.surroundings, self.display = obj.nextnodes, obj.surroundings, obj.display

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
                if node not in [explored, self.Initial, self.Goal]:
                    self.Base[node[0]][node[1]] = 2
                    explored.append(node)

                    # 3. Neighbor gathering and pathfinding process termination evaluation
                    for neighbor in self.nextnodes(node):
                        if self.Base[neighbor[0]][neighbor[1]] == 1 and neighbor not in [explored, frontier]:
                            frontier.append(neighbor)
                        elif self.Base[neighbor[0]][neighbor[1]] == 10:
                            te = time()
                            print(f"Array modified correctly. Time elapsed: {format(te - ts, '.4f')}s")
                            return 1
            
            # If there are no nodes to be explored (no solution)
            else:
                return 0

maze = Maze(); maze.basegenerator((20, 60)); maze.pathgenerator()
maze.display()

solve = Solver(maze); solve.solve_1(); solve.display()
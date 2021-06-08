from maze_generator import Maze
from maze_solver import Solver

# Array size definition:

Xsize = 30
Ysize = 30

# Array generation and display:

test = Maze()
test.basegenerator((Xsize, Ysize))
test.pathgenerator()
test.display()

# Path finding and display:

solved_test = Solver(test)
solved_test.solve_2()
solved_test.display()

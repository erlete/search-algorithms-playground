"""Various tests for the 'main.py' file."""

from main import Maze


def generator(size=(40, 40)):
    """Base path generator test."""
    obj = Maze(size)
    obj.pathgenerator()
    print(obj)


def solver_1(size=(40, 40)):
    """DFS search algorithm test."""
    obj = Maze(size)
    obj.pathgenerator()
    print(obj)

    obj.dfs()
    print(obj)


def solver_2(size=(40, 40)):
    """GBFS search algorithm test."""
    obj = Maze(size)
    obj.pathgenerator()
    print(obj)

    obj.gbfs()
    print(obj)


generator((40, 80))
solver_1((40, 80))
solver_2((40, 80))

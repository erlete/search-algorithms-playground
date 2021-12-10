"""Various tests for the 'main.py' file."""

from main import Maze, Node
from time import time
import matplotlib.pyplot as plt


DIMENSIONS = (20, 20)
VERBOSE = False


def test_1(size = DIMENSIONS, verbose = VERBOSE):
    """Instance creation test with ASCII representation."""

    print("\nTEST 1")

    obj = Maze(size, verbose=verbose)
    print(obj)


def test_2(size = DIMENSIONS, verbose = VERBOSE):
    """Path generation test with ASCII representation."""

    print("\nTEST 2")

    obj = Maze(size, verbose=verbose)
    obj.path_generator()

    print(obj)


def test_3(size = DIMENSIONS, verbose = VERBOSE):
    """Path generation test with image representation."""

    print("\nTEST 3")

    obj = Maze(size, verbose=verbose)
    obj.path_generator()

    obj.display()


def test_4(size = DIMENSIONS, verbose = VERBOSE):
    """Path solving (DFS) with ASCII and image representation"""

    print("\nTEST 4")

    obj = Maze(size, verbose=verbose)
    obj.path_generator()
    obj.dfs()

    print(obj)
    obj.display()


def test_5(size = DIMENSIONS, verbose = VERBOSE):
    """Path solving (GBFS) with ASCII and image representation"""

    print("\nTEST 5")

    obj = Maze(size, verbose=verbose)
    obj.path_generator()
    obj.gbfs()

    print(obj)
    obj.display()


def test_6(cycles = 5, verbose = VERBOSE):
    """Visual benchmarking utility."""

    x_axis = range(2, cycles)
    y_axis_1, y_axis_2 = [], []

    for iteration in x_axis:
        obj = Maze((iteration, iteration), verbose=verbose)

        timer_start = time()
        obj.path_generator()
        timer_mid = time()
        obj.gbfs()
        timer_end = time()

        y_axis_1.append(timer_mid - timer_start)
        y_axis_2.append(timer_end - timer_mid)

    curve_1 = plt.plot(x_axis, y_axis_1, color="orange")
    curve_2 = plt.plot(x_axis, y_axis_2, color="black")

    plt.show()


if __name__ == "__main__":
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    test_5(size=(20, 20), verbose=True)
    # test_6(60)

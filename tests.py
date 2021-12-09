"""Various tests for the 'main.py' file."""

from main import Maze, Node
from time import time
from math import log, sqrt
import matplotlib.pyplot as plt


DIMENSIONS = (20, 20)
VERBOSE = True


def test_1(size=DIMENSIONS, verbose=VERBOSE):
    """Instance creation test with ASCII representation."""

    print("\nTEST 1")

    obj = Maze(size)
    print(obj)


def test_2(size=DIMENSIONS, verbose=VERBOSE):
    """Path generation test with ASCII representation."""

    print("\nTEST 2")

    obj = Maze(size)
    obj.path_generator()

    print(obj)


def test_3(size=DIMENSIONS, verbose=VERBOSE):
    """Path generation test with image representation."""

    print("\nTEST 3")

    obj = Maze(size)
    obj.path_generator()

    obj.display()


def test_4(size=DIMENSIONS, verbose=VERBOSE):
    """Path solving (DFS) with ASCII and image representation"""

    print("\nTEST 4")

    obj = Maze(size)
    obj.path_generator()
    obj.dfs()

    print(obj)
    obj.display()


def test_5(size=DIMENSIONS, verbose=VERBOSE):
    """Path solving (GBFS) with ASCII and image representation"""

    print("\nTEST 5")

    obj = Maze(size)
    obj.path_generator()
    obj.gbfs()

    print(obj)
    obj.display()


def test_6(mode="log"):
    """Benchmarking utility.

    Modes: "lin", "log", "sqrt".
    """
    top = 0
    dimensions = (top + 2, top + 2)
    path, search, path_limit, search_limit = 0, 0, 0.1, 0.1
    registry = {}
    CYCLES = 200

    y_1 = []
    y_2 = []
    y_3 = []
    y_4 = []

    while path < path_limit and search < search_limit:
    # for c in range(CYCLES):

        print(f"Cycle: {top}")
        # print(f"\nDimensions: {dimensions}")
        # print(f"Path limit: {path_limit}s :: Search limit: {search_limit}s")

        # if input("Continue (Y/n): ").lower() == 'n':
        #     break

        obj = Maze(dimensions)

        path_timer_start = time()
        obj.path_generator()
        path_timer_end = time()

        search_timer_start = time()
        obj.gbfs()
        search_timer_end = time()

        path = path_timer_end - path_timer_start
        search = search_timer_end - search_timer_start

        registry[top] = {
            "path_limit": path_limit,
            "path_time": path,
            "search_limit": search_limit,
            "search_time": search
        }

        y_1.append(path)
        y_2.append(path_limit)
        y_3.append(search)
        y_4.append(search_limit)

        top += 1
        dimensions = (top + 2, top + 2)

        if mode == "lin":
            path_limit = 3 * top / 2
            search_limit = top

        elif mode == "log":
            top = top if log(top) != 0 else top + 1
            path_limit = 3 * log(top) / 2
            search_limit = log(top)

        elif mode == "sqrt":
            path_limit = 3 * sqrt(top) / 2
            search_limit = sqrt(top)

    x = list(range(top))
    plt.plot(x, y_1, color="red")
    plt.plot(x, y_2, color="orange")
    plt.plot(x, y_3, color="blue")
    plt.plot(x, y_4, color="green")

    plt.show()

    print(f"\nMax cycles: {top}")
    print(f"Path limit: {path_limit:.5}s :: Path elapsed: {path}s")
    print(f"Search limit: {search_limit:.5}s :: Search elapsed: {search}s")


if __name__ == "__main__":
    # test_1()
    # test_2()
    # test_3()
    # test_4()
    # test_5()
    test_6()

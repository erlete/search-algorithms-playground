"""Various tests for the 'main.py' file."""

from main import Maze, Node
from time import time
import matplotlib.pyplot as plt

CONSTANTS = {
    "dimensions": (20, 20), "logger": 1, "cycles": 50, "show_image": 1,
    "save_image": 0
}


def test_1(size=CONSTANTS["dimensions"], logger=CONSTANTS["logger"]):
    """Instance creation test with ASCII representation."""

    print("\nTEST 1")

    obj = Maze(size, logger=logger)
    print(obj)


def test_2(size=CONSTANTS["dimensions"], logger=CONSTANTS["logger"]):
    """Path generation test with ASCII representation."""

    print("\nTEST 2")

    obj = Maze(size, logger=logger)
    obj.path_generator()

    print(obj.ascii())


def test_3(size=CONSTANTS["dimensions"], show_image=CONSTANTS["show_image"],
        save_image=CONSTANTS["save_image"], logger=CONSTANTS["logger"]):
    """Path generation test with image representation."""

    print("\nTEST 3")

    obj = Maze(size, logger=logger)
    obj.path_generator()

    obj.image()


def test_4(size=CONSTANTS["dimensions"], show_image=CONSTANTS["show_image"],
        save_image=CONSTANTS["save_image"], logger=CONSTANTS["logger"]):
    """Path solving (DFS) with ASCII and image representation"""

    print("\nTEST 4")

    obj = Maze(size, logger=logger)
    obj.path_generator()
    obj.dfs()

    print(obj.ascii())
    obj.image()


def test_5(size=CONSTANTS["dimensions"], show_image=CONSTANTS["show_image"],
        save_image=CONSTANTS["save_image"], logger=CONSTANTS["logger"]):
    """Path solving (GBFS) with ASCII and image representation"""

    print("\nTEST 5")

    obj = Maze(size, logger=logger)
    obj.path_generator()
    obj.gbfs()

    print(obj.ascii())
    obj.image()


def test_6(cycles=CONSTANTS["cycles"], logger=False):
    """Visual benchmarking utility (path generation vs search methods)."""

    x_axis = range(3, cycles)
    y_axis_1, y_axis_2, y_axis_3 = [], [], []

    for iteration in x_axis:
        obj = Maze((iteration, iteration), logger=logger)

        time_0 = time()
        obj.path_generator()
        time_1 = time()
        obj.dfs()
        time_2 = time()
        obj.gbfs()
        time_3 = time()

        y_axis_1.append(time_1 - time_0)
        y_axis_2.append(time_2 - time_1)
        y_axis_3.append(time_3 - time_2)

    curve_1, = plt.plot(x_axis, y_axis_1, color="black", label="Path generation")
    curve_2, = plt.plot(x_axis, y_axis_2, color="orange", label="Depth-First Search")
    curve_3, = plt.plot(x_axis, y_axis_3, color="red", label="Greedy Best-First Search")

    plt.title("Elapsed times comparison")
    plt.xlabel("Order of dimensions")
    plt.ylabel("Time elapsed (s)")
    plt.legend(loc="center left")

    plt.show()


def test_6(cycles=CONSTANTS["cycles"], logger=False):
    """Visual benchmarking utility (search methods)."""

    x_axis = range(3, cycles)
    y_axis_1, y_axis_2 = [], []

    for iteration in x_axis:
        obj = Maze((iteration, iteration), logger=logger)
        obj.path_generator()

        time_0 = time()
        obj.dfs()
        time_1 = time()
        obj.gbfs()
        time_2 = time()

        y_axis_1.append(time_1 - time_0)
        y_axis_2.append(time_2 - time_1)

    curve_1, = plt.plot(x_axis, y_axis_1, color="orange", label="Depth-First Search")
    curve_2, = plt.plot(x_axis, y_axis_2, color="red", label="Greedy Best-First Search")

    plt.title("Elapsed times comparison")
    plt.xlabel("Order of dimensions")
    plt.ylabel("Time elapsed (s)")
    plt.legend(loc="center left")

    plt.show()


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()

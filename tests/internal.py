"""Various tests for the 'main.py' file."""

from utils.maze import Maze
from time import perf_counter
import matplotlib.pyplot as plt


CONFIG = {
    "dimensions": (20, 20),
    "cycles": 50,
    "verbose": True
}


def log(message: str):
    """Prints a message if the verbose option is enabled."""

    if CONFIG["verbose"]:
        print(message)


def generation_test():
    """Ensures that the maze is correctly generated."""

    log(" · Generation test started...")
    cron_start = perf_counter()
    Maze(CONFIG.get("dimensions"))
    log(f" > Maze generated in {perf_counter() - cron_start:.4}s.\n")


def ascii_test():
    """Ensures that the ASCII representation works correctly."""

    log(" · ASCII test started...")
    maze = Maze(CONFIG.get("dimensions"))
    log(maze.ascii())
    log(" > ASCII representation finished.\n")


def image_show_test():
    """Ensures that the image is correctly shown."""

    log(" · Image show test started...")
    maze = Maze(CONFIG.get("dimensions"))
    maze.image(True, False)
    log(" > Image display finished.\n")


def image_save_test():
    """Ensures that the image is correctly saved."""

    log(" · Image save test started...")
    maze = Maze(CONFIG.get("dimensions"))
    maze.image(False, True)
    log(" > Image saving finished.\n")


def depth_first_search_test():
    """Ensures that the depth-first search algorithm works correctly."""

    log(" · DFS test started...")
    cron_start = perf_counter()
    maze = Maze(CONFIG.get("dimensions"))
    maze.depth_first_search()
    log(f" > DFS finished in {perf_counter() - cron_start:.4}s.\n")


def breadth_first_search_test():
    """Ensures that the breadth-first search algorithm works correctly."""

    log(" · BFS test started...")
    cron_start = perf_counter()
    maze = Maze(CONFIG.get("dimensions"))
    maze.breadth_first_search()
    log(f" > BFS finished in {perf_counter() - cron_start:.4}s.\n")


def greedy_best_first_search_test():
    """Ensures that the greedy best-first search algorithm works correctly."""

    log(" · GBFS test started...")
    cron_start = perf_counter()
    maze = Maze(CONFIG.get("dimensions"))
    maze.greedy_best_first_search()
    log(f" > GBFS finished in {perf_counter() - cron_start:.4}s.\n")


def main():
    """Main function for tests."""

    log(" ·Tests started...")
    generation_test()
    ascii_test()
    image_show_test()
    image_save_test()
    depth_first_search_test()
    breadth_first_search_test()
    greedy_best_first_search_test()
    log(" > Tests finished.")

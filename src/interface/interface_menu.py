"""Container for the InterfaceMenu class.

The InterfaceMenu class is intended to be a plug-in to the Menu class that
contains repository-specific methods for the menu interface.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


from time import perf_counter

from utils.interface.menu import Menu
from utils.internal.maze import Maze


# Auxiliary methods:


def inputn(text: str) -> None:
    """Generates a data input prompt and prints a newline after it."""

    input_data = input(text)
    print()
    return input_data


# Module classes:


class InterfaceMenu(Menu):
    """Interface menu for maze generation, search and result display."""

    def __init__(self):
        super().__init__()
        self.maze = None

    def generate_maze(self):
        """Interface for maze generation."""

        x = int(input("  · Enter the maze width: "))
        y = int(inputn("  · Enter the maze height: "))

        print("  · Generating maze...")
        cron = perf_counter()
        self.maze = Maze((x, y))
        print(
            f"  · Maze generated successfully ({perf_counter() - cron:.4}s)\n")

    def df_search(self):
        """Interface for depth-first search."""

        print("  · Depth-first search...")
        cron = perf_counter()
        self.maze.depth_first_search()
        print(
            f"  · Depth-first search completed successfully ({perf_counter() - cron:.4}s)\n")

    def bf_search(self):
        """Interface for breadth-first search."""

        print("  · Breadth-first search...")
        cron = perf_counter()
        self.maze.breadth_first_search()
        print(
            f"  · Breadth-first search completed successfully ({perf_counter() - cron:.4}s)\n")

    def gbf_search(self):
        """Interface for greedy-best-first search."""

        print("  · Greedy best-first search...")
        cron = perf_counter()
        self.maze.greedy_best_first_search()
        print(
            f"  · Greedy best-first search completed successfully ({perf_counter() - cron:.4}s)\n")

    def r_search(self):
        """Interface for radial search."""

        print("  · Radial search...")
        cron = perf_counter()
        self.maze.radial_search()
        print(
            f"  · Radial search completed successfully ({perf_counter() - cron:.4}s)\n")

    def display_ascii(self):
        """Interface for ASCII maze display."""

        print("  · Displaying maze in ASCII format...")
        print(self.maze.ascii())
        print("  · Maze displayed successfully\n")

    def display_image(self):
        """Interface for maze image display."""

        print("  · Displaying maze in image format...")
        self.maze.image(True, False)
        print("  · Maze displayed successfully\n")

    def save_image(self):
        """Interface for maze image saving."""

        print("  · Saving maze image...")
        self.maze.image(False, True)
        print("  · Maze image saved successfully\n")

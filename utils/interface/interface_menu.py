"""Container for the InterfaceMenu class, specifically designed for the
interface used on the Archive project.

Author:
------
Paulo Sanchez (dev.szblzpaulo@gmail.com)
"""


from utils.interface.menu import Menu


def inputn(text: str) -> None:
    """Generates a data input prompt and prints a newline after it."""

    input_data = input(text)
    print()
    return input_data


class InterfaceMenu(Menu):
    pass

"""Menu utilities module.

Provides with command line based menu functionality, implementing several
methods that allow menu entry addition, removal or even statement execution
linked to a specific option.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


class MenuItem:
    """Represents an item of a Menu.

    Parameters:
    -----------
     - title : str
        The title of the menu item, which will be displayed when the MenuItem
        object is called.
     - callback_function : callable_function_or_method
        The method that will be called when the MenuItem is selected from the
        menu.

    Note:
    -----
    This class implements getter and setter methods for both title and
    callback function of its instances.
    """

    def __init__(self, title: str, callback_function=None,
                 section_end: bool = False, section_title: str = None):
        self.__title = title
        self.__callback_function = callback_function
        self.__section_end = section_end
        self.__section_title = section_title

    @property
    def title(self):
        return self.__title

    @property
    def callback_function(self):
        return self.__callback_function

    @property
    def section_end(self):
        return self.__section_end

    @property
    def section_title(self):
        return self.__section_title

    @title.setter
    def title(self, title: str):
        if isinstance(title, str):
            self.__title = title
        else:
            raise TypeError("title must be a str object.")

    @callback_function.setter
    def callback_function(self, callback_function):
        if callable(function):
            self.__callback_function = callback_function
        else:
            raise TypeError("function must be a callable object.")

    @section_end.setter
    def section_end(self, section_end):
        self.__section_end = section_end

    @section_title.setter
    def section_title(self, section_title: str):
        if isinstance(section_title, str):
            self.__section_title = section_title
        else:
            raise TypeError("section title must be a str object.")

    def __len__(self):
        """Returns the length of the title of the MenuItem object."""
        return len(self.__title)

    def __str__(self):
        """Returns the title of the MenuItem object, capitalized."""

        return self.__title.capitalize()


class Menu:
    """Represents a collection of menu items.

    Provides with item addition and removal methods, as well as searching
    functionality by title or index. Also implements a fine printing
    representation.

    Note:
    -----
    Once instantiated, the add_item method must be used to add items
    to the menu.
    """

    # Fine printing settings:

    FILLER = '–'
    CORNER = 'ø'

    def __init__(self):
        self.__MENU_ITEMS = []

    def add_item(self, *items) -> None:
        """Adds a collection of items to the menu."""

        for item in items:
            if isinstance(item, MenuItem):
                self.__MENU_ITEMS.append(item)

    def remove_item(self, item: MenuItem) -> None:
        """Removes an item from the menu."""

        del self.__MENU_ITEMS[self.__MENU_ITEMS.find(item)]

    def get_by_index(self, index: int) -> MenuItem:
        """Returns an item that matches the specified index."""

        if 0 <= index < len(self.__MENU_ITEMS):
            return self.__MENU_ITEMS[index]

        raise IndexError("no item matches the specified index.")

    def get_by_title(self, title: str) -> MenuItem:
        """Returns an item that matches the specified title."""

        for item in self.__MENU_ITEMS:
            if item.title == title:
                return item

        raise KeyError("no item matches the specified title.")

    def execute(self, item: MenuItem) -> None:
        """Executes the specified item's function."""

        item.callback_function()

    def __separator(self, text=None):
        """Returns a visual separator."""

        text = f" {text} " if text else ''

        padding = len(
            max(self.__MENU_ITEMS, key=lambda item: len(item))
        ) + 10

        return '\n' + self.CORNER + text.center(
            padding - 2 * len(self.CORNER) + 2, self.FILLER
        ) + self.CORNER + "\n\n"

    def display(self, index_offset: int = 0):
        """Returns a fine-printed, indexed representation of the menu. The
        index offset determines the index value from which the index counter
        starts.
        """

        output = (
            f"  · {index + index_offset:2} · {item}\n" + (
                self.__separator(item.section_title)
                if item.section_end else ''
            ) for index, item in enumerate(self.__MENU_ITEMS)
        )

        print(
            self.__separator("Main menu")
            + ''.join(output)
            + self.__separator()
        )

    def __len__(self):
        """Returns the amount of items in the menu."""

        return len(self.__MENU_ITEMS)

"""Main interface module for simple user interaction.

This module allows the user to interact with the program through a simple
command line interface. It provides functions to generate a maze, search
it and display the results in several ways.

Author:
------
 - Paulo Sánchez (@erlete)
"""


import os

from utils.interface.interface_menu import InterfaceMenu
from utils.interface.menu import MenuItem


# Configuration constants:

INDEX_OFFSET = 1

# Object instantiation:

MENU = InterfaceMenu()
MENU.add_item(
    MenuItem("Exit interface")
)

# Mainloop:

active = True

while active:
    os.system("clear")
    MENU.display(index_offset=INDEX_OFFSET)

    try:
        option = input("  · Select an option: ")
        print()

        # Non-digit entry check:
        if option.isdigit():
            option = int(option)

            # Out of bounds entry check:
            if INDEX_OFFSET <= option <= len(MENU):
                item = MENU.get_by_index(option - INDEX_OFFSET)
                os.system("clear")
                print(f" Executing \"{item}\" ".center(90, '–') + '\n')

                # Existing callback function check:
                if item.callback_function is not None:
                    MENU.execute(item)

                else:
                    active = False
            else:
                print("Invalid index value, try again...\n")
        else:
            print("Not an index value, try again...\n")

    # Forced exit:
    except KeyboardInterrupt:
        active = False

    # Unclassified exception report:
    except Exception as exception:
        print(f"Unclassified error. Report: {exception}\n")

    finally:
        if active:
            input(" Enter to continue... ".center(90, '–'))  # Display stop.
        else:
            exit()

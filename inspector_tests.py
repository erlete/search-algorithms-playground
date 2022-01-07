from inspector import Inspector, DEFAULTS
from time import time


class Interface:
    def __init__(self):
        self.start = self.set_attribute("start", lower_bound=2)
        self.cycles = self.set_attribute("cycles")
        self.constant = self.set_attribute("constant", is_bool=True)
        self.show_image = self.set_attribute("show_image", is_bool=True)
        self.save_image = self.set_attribute("save_image", is_bool=True)
        self.logger = self.set_attribute("logger", is_bool=True)

        self.global_command = False

        timer = time()
        print("\nGenerating objects...")

        self.object = Inspector(cycles=self.cycles, start=self.start,
                                constant=self.constant, logger=self.logger)

        print(f"Done ({(time() - timer):.5}s).\n")

        timer = time()
        print("Performing initial benchmark...")

        self.object.benchmark()

        print(f"Done ({(time() - timer):.5}s).\n")

    def set_global(self):
        self.global_command = True

    def set_attribute(self, identifier, lower_bound=0, is_bool=False):
        try:
            if is_bool:
                return input(f"[{identifier.title()}] (Y/n) :: ").lower() in ('y', '1')

            option = int(
                input(f"[{identifier.title()}] Integer value greater than {lower_bound} :: "))
            assert option > lower_bound
            return option

        except Exception:
            print("Invalid format. Switching to default value...")
            return DEFAULTS[identifier]

    def handler(self, method, arguments=''):
        def temp():
            if self.global_command:
                for _ in self.object.mazes:
                    exec(f"maze['maze'].{method}({arguments})")
                self.global_command = False
            else:
                try:
                    index = int(input("Input an index: "))
                    print(
                        f"self.object.mazes[{index}]['maze'].{method}({arguments})")
                    exec(
                        f"self.object.mazes[{index}]['maze'].{method}({arguments})")
                except Exception:
                    print("[ERROR]: Invalid index. Returning to menu...")

        return temp

    def list(self):
        for index, maze in enumerate(sorted(
                self.object.mazes, reverse=True,
                key=lambda x: x["ratio"])):
            maze["index"] = index
            self.object.display(maze)

    def highest_ratio(self):
        self.object.display(max(self.object.mazes, key=lambda x: x["ratio"]))

    def lowest_ratio(self):
        self.object.display(min(self.object.mazes, key=lambda x: x["ratio"]))

    def image_handler(self):
        if self.global_command:
            for maze in self.object.mazes:
                maze["maze"].image(
                    show_image=self.show_image, save_image=self.save_image
                )
            self.global_command = False
        else:
            try:
                index = int(input("Input an index: "))
                assert 0 <= index <= len(self.object.mazes)
                self.object.mazes[index]["maze"].image(
                    show_image=self.show_image, save_image=self.save_image
                )
            except Exception:
                print("[ERROR]: Invalid index. Returning to menu...")


# Interface base:

interface = Interface()

options = (
    ("Benchmark utility", interface.object.benchmark),
    ("Comparison plot display", interface.object.display_plot),
    ("Display maze on image", interface.image_handler),
    ("Generated mazes' list", interface.list),
    ("Get the lowest ratio maze", interface.lowest_ratio),
    ("Get the highest ratio maze", interface.highest_ratio),
    ("Perform DF search", interface.handler("dfs")),
    ("Perform GBF search", interface.handler("gbfs")),
    ("Perform RS search", interface.handler("rs")),
    ("Perform next action over all mazes", interface.set_global),
    ("Exit: ", quit)
)

# Interface's mainloop:

while True:
    print("\nMenu:")
    for index, option in enumerate(options):
        print(f"{index + 1} :: {option[0]}")

    try:
        index = int(input("\nSelect an index: ")) - 1
        assert index >= 0
        options[index][1]()
    except IndexError:
        print("[ERROR]: Invalid index, try again...")
    except Exception:
        print("[ERROR]: Undefined error exception. Fatal crash.")
        quit()

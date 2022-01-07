from main import Maze, Node
import matplotlib.pyplot as plt


DEFAULTS = {
    "start": 10, "cycles": 1, "constant": 1, "logger": 0,
    "show_image": 1, "save_image": 0
}


class Inspector:
    def __init__(self, start=DEFAULTS["start"], cycles=DEFAULTS["cycles"],
                 constant=DEFAULTS["constant"], ratio=1,  # FIXME
                 logger=DEFAULTS["logger"]):

        self.cycles = cycles
        self.start = start
        self.constant = constant
        self.ratio = ratio

        self.x_axis, self.y_axis = [], []
        self.mazes = []

        self.logger = logger

    def benchmark(self):
        self.x_axis, self.y_axis, self.mazes = [], [], []

        for iteration in range(self.start, self.start + self.cycles):
            dimension = iteration if not self.constant else self.start
            obj = Maze((dimension, dimension), logger=self.logger)
            obj.path_generator()

            path = sum([1 if node.state == 1 else 0 for node in obj.node_map])
            total = iteration ** 2
            ratio = path ** 2 / total

            self.mazes.append({
                "index": len(self.mazes),
                "generation_order": iteration - self.start,
                "maze": obj,
                "path": path,
                "total": total,
                "ratio": ratio
            })

            self.x_axis.append(total)
            self.y_axis.append(ratio)

        self.mazes = sorted(self.mazes, key=lambda x: x["ratio"], reverse=True)

    def display_plot(self, real_plot_color="black", ideal_plot_color="green"):  # FIXME
        if self.constant:
            self.x_axis = range(self.cycles)

        plt.plot(self.x_axis, self.y_axis, color=real_plot_color)
        plt.plot(self.x_axis, [
            self.ratio for _ in range(self.start, self.cycles + self.start)
        ], color=ideal_plot_color)

        plt.grid()
        if self.constant:
            plt.xlabel("Object's index")
        else:
            plt.xlabel("Total tiles")
        plt.ylabel("(Path tiles) ^ 2 / Total tiles")

        plt.show()

    def list(self, ascending_ratio=True):
        maze_list = sorted(
            self.mazes, key=lambda x: x["ratio"], reverse=ascending_ratio)
        for index, maze in enumerate(maze_list):
            maze["index"] = index
            self.display(maze)

    def display(self, maze):
        print(f"""
Index: {maze["index"]}
	Generation order: {maze["generation_order"]}
	Maze object:      {maze["maze"]}
	Path:             {maze["path"]}
	Total:            {maze["total"]}
	Ratio:            {maze["ratio"]}
""")

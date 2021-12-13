from simple_maze import Maze

obj = Maze((20, 20), logger=False)
print(obj.ascii())

obj.path_generator()
print(obj.ascii())

obj.gbfs()
print(obj.ascii())

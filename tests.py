from main import Maze

def genTest(size = (40, 40)):
    obj = Maze(size)
    obj.pathgenerator()
    print(obj)    

def solveTest1(size = (40, 40)):
    obj = Maze(size)
    obj.pathgenerator()
    print(obj)

    obj.dfs()
    print(obj)

def solveTest2(size = (40, 40)):
    obj = Maze(size)
    obj.pathgenerator()
    print(obj)

    obj.gbfs()
    print(obj)

genTest((40, 80))
solveTest1((40, 80))
solveTest2((40, 80))

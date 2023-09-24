from MazeworldProblem import MazeworldProblem
from Maze import Maze
from astar_search import sensorless_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


# Test problems
test_maze3 = Maze("maze5.maz")
test_mp = SensorlessProblem(test_maze3, (7, 6, 7, 5, 6, 5))      #loaded maze, goals
print(test_maze3)
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result)
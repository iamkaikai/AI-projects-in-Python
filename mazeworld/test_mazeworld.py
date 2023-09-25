from MazeworldProblem import MazeworldProblem
from SensorlessProblem import SensorlessProblem
from Maze import Maze
from astar_search import astar_search
from astar_search_sensorless import astar_search_sensorless

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems
# test_maze3 = Maze("maze3.maz")
# test_mp = MazeworldProblem(test_maze3, (7, 6, 7, 5, 6, 5))      #loaded maze, goals
# print(test_maze3)

# uniform-cost search
# result = astar_search(test_mp, null_heuristic)
# print(f'result = {result}')

# load maze4 for testing
# test_maze4 = Maze("maze4.maz")
# test_mp = MazeworldProblem(test_maze4, (6, 1, 6, 2, 6, 0))      #loaded maze, goals
# print(test_maze4)

# this should do a bit better:
# result = astar_search(test_mp, test_mp.manhattan_heuristic)
# print(result)
# test_mp.animate_path(result)

# Test Sensorless
test_maze_sensorless = Maze("maze3.maz")
test_sp = SensorlessProblem(test_maze_sensorless)
result = astar_search_sensorless(test_sp, test_sp.manhattan_heuristic_max)
print(test_maze_sensorless)
print(result)
test_sp.animate_path(result)

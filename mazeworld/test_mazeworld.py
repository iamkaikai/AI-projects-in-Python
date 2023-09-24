from MazeworldProblem import MazeworldProblem
from Maze import Maze
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems
test_maze3 = Maze("maze3.maz")
test_mp = MazeworldProblem(test_maze3, (7, 6, 7, 5, 6, 5))      #loaded maze, goals
print(test_maze3)
# print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
# result = astar_search(test_mp, null_heuristic)
# print(f'result = {result}')

# load maze4 for testing
# test_maze4 = Maze("maze4.maz")
# test_mp = MazeworldProblem(test_maze4, (6, 1, 6, 2, 6, 0))      #loaded maze, goals
# print(test_maze4)

# this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result)

# Your additional tests here:

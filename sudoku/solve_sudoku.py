from display import display_sudoku_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    ############################ select solver ############################
    # result = sat.walkSAT()
    # result = sat.GSAT()
    result = sat.DPLL_SAT()

    if result:
        sat.write_solution(result, sol_filename)
        display_sudoku_solution(sol_filename)
from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        
    def __str__(self):
        string =  "Blind robot problem: "
        return string

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(0.5)
            print(str(self.maze))

    

## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze5.maz")
    print(test_maze3)
    test_problem = SensorlessProblem(test_maze3)
    print(test_problem)

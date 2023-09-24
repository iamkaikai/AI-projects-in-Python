from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        
    def __str__(self):
        string =  "Blind robot problem: "
        return string

    def generate_start_state(self):
        map = self.maze.map
        map_w = self.maze.width
        map_h = self.maze.height
        print(map_w, map_h)
        count = 0
       
       
        for i in map:
            x = count % map_w
            y = map_h - (count // map_w) -1
            print(x,y)
            # if i == '.':
                
            count += 1
       
        
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
    test_problem.generate_start_state()
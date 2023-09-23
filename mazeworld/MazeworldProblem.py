from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal = goal_locations
        self.start_state = maze.robotloc
        

    def __str__(self):
        string =  "Mazeworld problem: "
        return string


    # given a sequence of states (including robot turn), modify the maze and print it out.
    #  (Be careful, this does modify the maze!)
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])
        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))

    # For each pair of coordinates in 'locations', return a list of valid successor coordinates based on defined actions.
    def get_successors(self, locations):
        print(locations)
        result = []
        cur_locs = [(locations[i], locations[i+1]) for i in range(0, len(locations), 2)]
        for cur_loc in cur_locs:
            x = cur_loc[0]
            y = cur_loc[1]
            print(f'local x = {x} y = {y}')
            actions = [(1,0),(0,1),(-1,0),(0,-1)]
            rs = [(x + action[0], y + action[1]) for action in actions]
            print(rs)
            r = [r for r in rs if (self.maze.is_floor(r[0], r[1]) and not self.maze.has_robot(r[0], r[1])) ]
            result.append(r)
        return result
        
        
## A bit of test code. You might want to add to it to verify that things
#  work as expected.
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_maze3)
    print(test_mp.get_successors((1, 0, 1, 1, 2, 1)))

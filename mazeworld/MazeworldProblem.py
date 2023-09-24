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
    def get_successors(self, location_arr):
        result = []
        moving_agent = location_arr[-1]
        x = location_arr[moving_agent*2]
        y = location_arr[moving_agent*2 + 1]
        print('-----------')
        print(location_arr)
        actions = [(1,0),(0,1),(-1,0),(0,-1)]
        next_moves = [(x + action[0], y + action[1]) for action in actions]
        for next_loc in next_moves:
            next_loc_x = next_loc[0]
            next_loc_y = next_loc[1]
            if self.maze.is_floor(next_loc_x, next_loc_y) and not self.maze.has_robot(next_loc_x, next_loc_y):
                location_arr_new = list(location_arr)
                location_arr_new[moving_agent*2] = next_loc_x
                location_arr_new[moving_agent*2+1] = next_loc_y
                result.append(tuple(location_arr_new)) 
        print(f'agent_loc_next: x = {result}')
        print('-----------')
        return result
        
        
## A bit of test code. You might want to add to it to verify that things
#  work as expected.
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_maze3)
    print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 0)))
    print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 1)))
    print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 2)))
from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        self.init_states = set()
        map = self.maze.map
        map_w = self.maze.width
        map_h = self.maze.height
        count = 0       
        for i in map:
            x = count % map_w
            y = map_h - (count // map_w) -1
            if i == '.':
                self.init_states.add((x,y))
            count += 1
        print(self.maze)
        
    def __str__(self):
        string =  "Blind robot problem: "
        return string
    
    def get_state(self):
        return self.init_states    
    
    def set_to_tuple(self, set):
        return tuple(item for tup in set for item in tup)            
    
    def animate_path(self, path):
        self.maze.robotloc = self.set_to_tuple(self.init_states)
        actions = {'N':(0,1), 'S':(0,-1), 'W':(-1,0), 'E':(1,0)}
        
        print(str(self))
        print(str(self.maze))
        
        for direction in path:
            new_location = []
            dx, dy = actions[direction]
            for i in range(0, len(self.maze.robotloc), 2):
                x, y = self.maze.robotloc[i], self.maze.robotloc[i+1]
                nx, ny = x + dx, y + dy
                if self.maze.is_floor(nx, ny):
                    new_location.extend([nx, ny])
                else:
                    new_location.extend([x, y])
            self.maze.robotloc = tuple(new_location)
            sleep(1)
            print(str(self.maze))

    def get_successors(self, states, direction):
        actions = {'N':(0,1), 'S':(0,-1), 'W':(-1,0), 'E':(1,0)}
        new_states = set()
        for state in states:        
            new_x = state[0] + actions[direction][0]
            new_y = state[1] + actions[direction][1]
            if self.maze.is_floor(new_x, new_y):
                new_states.add((new_x, new_y))
            else:
                new_states.add(state)
        return new_states
    
    def heuristic(self, states):
        return len(states)
    
## A bit of test code

if __name__ == "__main__":
    test_maze5 = Maze("maze5.maz")
    print(test_maze5)
    test_problem = SensorlessProblem(test_maze5)
    s = test_problem.get_successors(test_problem.get_state(), 'S')
    print(test_problem.get_state())
    print(s)
import random

class Maze:
    def __init__(self):
        self.maze = []
        self.width = 2      # include the edge
        self.height = 2     # include the edge
        
    def __str__(self) -> str:
        maze_str = ''
        for row in self.maze:
            maze_str += ' '.join([cell.ljust(1) for cell in row]) + '\n'
        return maze_str
    
    def generate_rand_maze(self, width, height):
        self.width += width
        self.height += height
        
        # Define the colors and the size of the maze
        colors = ['R', 'G', 'B', 'Y']

        # Initialize the nxn maze with empty cells
        maze = [['.' for col in range(width)] for row in range(height)]

        # Assign a random color to each cell
        for i in range(height):
            for j in range(width):
                maze[i][j] = random.choice(colors)

        # Insert wall for ASCII art
        self.maze = maze
        self.maze.insert(0, ['#' for _ in range(width)])
        self.maze.insert(height+1, ['#' for _ in range(width)])
        for row in self.maze:
            row.insert(0,'#')
            row.insert(width+1,'#')
    
    def insert_wall_in_maze(self, row, col):
        self.maze[row][col] = '#'

class Robot:
    def __init__(self, maze):
        self.belief_state = []
        self.maze = maze
        self.transition_model = {}
        self.sensor_model = {}
        
    def generate_states(self):
        total_grid = 0
        for row in self.maze.maze:
            for col in row:
                if col != '#':
                    total_grid +=1
        self.belief_state = [1/total_grid for _ in range(total_grid)]
        print(f'\ntotal grid = {total_grid}')
        print(f'belief_state:{self.belief_state}')
        
    def generate_transition_model(self):
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                if self.maze.maze[row][col] == '#':
                    continue
                self.transition_model[(row, col)] = {
                    'N': {(row - 1, col): 0.25} if self.maze.maze[row - 1][col] != '#' else {(row, col): 0.25},
                    'S': {(row + 1, col): 0.25} if self.maze.maze[row + 1][col] != '#' else {(row, col): 0.25},
                    'W': {(row, col - 1): 0.25} if self.maze.maze[row][col - 1] != '#' else {(row, col): 0.25},
                    'E': {(row, col + 1): 0.25} if self.maze.maze[row][col + 1] != '#' else {(row, col): 0.25}
                }
    
        print(f'\ntransition_model:')
        for key, value in self.transition_model.items():
            print(key,value)

    def generate_sensor_model(self):
        colors = ['R', 'G', 'B', 'Y']
        for color in colors:
            self.sensor_model[color] = {c: 0.88 if c == color else 0.04 for c in colors}
        print(f'\nsensor_model{self.sensor_model}')
        
    def predict(self):
        new_belief_state = [0 for _ in range(len(self.belief_state))]
        row_col_to_belief_state = {(row, col): index for index, (row, col) in enumerate(self.transition_model)}
        print(f'row_col_to_belief_state: {row_col_to_belief_state}')
        
    
    def update(self):
        pass
    
    def filter(self, sensor):
        for color in sensor:
            self.predict()
            self.update(color)
            
import random
import copy

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

    def print_best_guest(self, row, col):
        new_maze = Maze()
        new_maze.maze = copy.deepcopy(self.maze.maze)
        new_maze.width = self.maze.width
        new_maze.height = self.maze.height
        new_maze.maze[row][col] = '●'
        
        # Split the string representations of the mazes into lists of lines
        map_display = ''
        for idx_row in range(self.maze.height):
            original_line = ' '.join(self.maze.maze[idx_row])
            new_line = ' '.join(new_maze.maze[idx_row])
            combined_line = original_line + ' ' * 4 + new_line
            map_display += combined_line + '\n'
        print(f'\n{map_display}')

        
    def position_to_belief_state(self, transition_model):
        return {(row, col): index for index, (row, col) in enumerate(transition_model)}
    
    def belief_state_to_position(self, index):
        for idx, pos in enumerate(self.transition_model):
            if index == idx:
                return pos
        
    def predict(self):
        new_belief_state = [0 for _ in range(len(self.belief_state))]
        row_col_to_belief_state = self.position_to_belief_state(self.transition_model)
        
        for (row, col), next_directions_prob in self.transition_model.items():  # (1, 1): {'N': {(1, 1): 0.25}, ...''E': {(1, 2): 0.25}}
            cur_index = row_col_to_belief_state[(row, col)]                     # (1, 1) - > 0
            for next_direction, transitions in next_directions_prob.items():    # 'N': {(1, 1): 0.25}, ...'E': {(1, 2): 0.25}}
                for (next_row, next_col), next_prob in transitions.items():     # (1, 1): 0.25
                    next_index = row_col_to_belief_state[(next_row, next_col)]  
                    if next_index is not None:
                        new_belief_state[next_index] += self.belief_state[cur_index] * next_prob
                    
        self.belief_state = new_belief_state    
                
    def update(self, reading_color):
        total_prob = 0
        for index, (row, col) in enumerate(self.transition_model):
            color = self.maze.maze[row][col]
            self.belief_state[index] *= self.sensor_model[reading_color][color]
            total_prob += self.belief_state[index]
        
        if total_prob != 1:
            self.belief_state = [value / total_prob for value in self.belief_state]
        
    
    def filter(self, reading_seq):
        for color in reading_seq:
            color = color.upper()
            self.predict()
            self.update(color)
        return self.belief_state
    
    def sensor_read(self, color_seq):
        max_prob = float('-inf')
        best_guest_row, best_guest_col = None, None
        
        belief_state = self.filter(color_seq)
        for idx, value in enumerate(belief_state):
            row, col = self.belief_state_to_position(idx)
            if belief_state[idx] > max_prob:
                max_prob = belief_state[idx]
                best_guest_row, best_guest_col = row, col
            print(f'({row}, {col}) = {format(belief_state[idx], ".16f")}')
        
        print(f'\n👉 most likely position: \n({best_guest_row}, {best_guest_col}) = {max_prob}  #(row, col)')
        self.print_best_guest(best_guest_row, best_guest_col)
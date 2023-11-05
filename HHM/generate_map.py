import random

# Define the colors and the size of the maze
colors = ['red', 'green', 'yellow', 'blue']
size = 4  # for a 4x4 maze

# Initialize the maze with empty cells
maze = [['' for _ in range(size)] for _ in range(size)]

# Assign a random color to each cell
for i in range(size):
    for j in range(size):
        maze[i][j] = random.choice(colors)

# Print the maze to verify
for row in maze:
    print(row)

from hmm import Maze, Robot


maze = Maze()
maze.generate_rand_maze(4, 4)
print(maze)

maze.insert_wall_in_maze(4,2)
maze.insert_wall_in_maze(1,3)
maze.insert_wall_in_maze(2,3)
maze.insert_wall_in_maze(2,2)
print(maze)

robot = Robot(maze)
robot.generate_states()
robot.generate_transition_model()
robot.generate_sensor_model()
robot.predict()
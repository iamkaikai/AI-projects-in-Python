from hmm import Maze, Robot


maze = Maze()
maze.generate_rand_maze(4, 4)
maze.insert_wall_in_maze(4,2)
maze.insert_wall_in_maze(1,3)
maze.insert_wall_in_maze(2,3)
maze.insert_wall_in_maze(2,2)

print(f'maze: \n{maze}')
color_seq = input('please enter your color sequence (e.g. R,G,R,R): ')
color_seq = color_seq.split(",")

robot = Robot(maze)
robot.generate_states()
robot.generate_transition_model()
robot.generate_sensor_model()

print(f'\ninput sequence = {color_seq}\n')
robot.sensor_read(color_seq)


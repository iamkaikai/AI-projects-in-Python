import numpy as np
import time
from robot import Robot

# R2 test
# start_config = [0, 1/4 * np.pi]
# end_config = [-1/2 * np.pi, -1/2 * np.pi]
# arm_length = [1,1]
# num_arm = 2

# R3 test
# start_config = [0, 1/4 * np.pi, 1/4 * np.pi]
# end_config = [-2/3 * np.pi, -1/2 * np.pi, -1.8/5 * np.pi]
# arm_length = [1,1,1.5]
# num_arm = 3

# R4 test
start_config = [0, 1/4 * np.pi, 1/4 * np.pi, 0]
end_config = [-2/3 * np.pi, -1/2 * np.pi, -1.8/5 * np.pi, 0]
arm_length = [1,1,1.5,1]
num_arm = 4

sample_sizes = [50000]
k_sizes = [4]

obstacles = [[(1,-1), (3,1), (3,-2), (1,-3), (0,-1.5), (1,-1)],
             [(1,1), (1,3), (-1,3), (-1,0), (1,1)],
             [(-1.5,2), (-1.5,-2), (-3,-3), (-3,2), (-1.5,2)]]

for sample_size in sample_sizes:
    for k_size in k_sizes:
        robot_3R = Robot(num_arm, arm_length, start_config, end_config)  # New Robot instance for each iteration
        for obstacle in obstacles:
            robot_3R.add_obstacle(obstacle)
        
        title = f'Sample Size: {sample_size}, K Size: {k_size}'
        robot_3R.fig.suptitle(title)
        start_time = time.time()  # Start timing
        robot_3R.sampling_config(sample_size, k_size)
        robot_3R.query_path()
        end_time = time.time()  # End timing

        print(f"{title}, runtime = {end_time - start_time} seconds")

        robot_3R.render_obstacles()
        robot_3R.animation()  

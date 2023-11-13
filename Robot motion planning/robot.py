import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import Polygon, LineString
from collections import deque

class Node:
    def __int__(self):
        self.pre = None
        self.cur = None
        
class Robot:
    def __init__(self, num_arms, arm_lengths, start_config, end_config):
        self.num_arms = num_arms
        self.arm_lengths = arm_lengths
        self.joints_angles = start_config
        self.goal_angles = end_config
        self.init_plot()
        self.obstacles = []
        self.joint_x = []
        self.joint_y = []
        self.start_config = start_config
        self.end_config = end_config
        self.graph = {}
        
    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'o-', lw=2)
        self.ax.set_xlim(-sum(self.arm_lengths), sum(self.arm_lengths))
        self.ax.set_ylim(-sum(self.arm_lengths), sum(self.arm_lengths))
       
    def kinematics(self, joints_thetas):
        x = [0]
        y = [0]
        for i in range(self.num_arms):
            if i < 1:
                x.append(x[-1] + self.arm_lengths[i] * np.cos(joints_thetas[i]))
                y.append(y[-1] + self.arm_lengths[i] * np.sin(joints_thetas[i]))
            else:
                x.append(x[-1] + self.arm_lengths[i] * np.cos(sum(joints_thetas[:i+1])))
                y.append(y[-1] + self.arm_lengths[i] * np.sin(sum(joints_thetas[:i+1])))
        return x, y

        
    def display(self):
        x,y = self.kinematics(self.joints_angles)
        self.line.set_data(x,y)
        plt.show()
        
    def update(self, frames):
        x, y = self.kinematics(self.joints_angles)
        self.line.set_data(x,y)
        return self.line,
    
    def add_vertex(self, config):
        if config not in self.graph:
            self.graph[config] = []
    
    def add_edge(self, v1, v2):
        if v2 not in self.graph[v1]:
            self.graph[v1].append(v2)
            
        if v1 not in self.graph[v2]:    
            self.graph[v2].append(v1)
    
    def collision_checker(self, config):
        x, y = self.kinematics(config)
        vertices = list(zip(x, y))
        self.arms = []
        for i in range(len(vertices)-1):
            self.arms.append(LineString([vertices[i], vertices[i+1]]))
        for arm in self.arms:
            for obstacle in self.obstacles:
                if arm.intersects(obstacle):
                    print(f'collision at {arm}')
                    return True    
        return False
    
    def euclidean_distance(self, config1, config2):
        return np.linalg.norm(np.array(config2) - np.array(config1))           
    
    def find_K_nearest_neighbors(self, cur_vertex, all_vertices, k=5):
        dist = [(other_v, self.euclidean_distance(cur_vertex, other_v)) for other_v in all_vertices if other_v != cur_vertex]
        dist.sort(key = lambda pair: pair[1])
        return [vertex for vertex, dist in dist[:k]]
        
    def A_star(self, graph, start, end):   
        start_node = None
        min_dist = float('inf')
        list = deque()
        list.append(tuple(start))
        
        def backTrack_path():
            
        
        # bfs
        while list:
            cur_node = list.popleft()
            if cur_node == tuple(end):
                return backTrack_path
            for value in cur_node:
                pass
            
    def path_finding(self, start, end):
        path = self.A_star(self.graph, start, end)
        return path
    
    def sampling_config(self, sample_size = 1000):
        min_theta = -np.pi*2
        max_theta = np.pi*2
        
        self.add_vertex(tuple(self.start_config))
        self.add_vertex(tuple(self.end_config))
        
        for _ in range(sample_size):
            random_config = [np.random.uniform(min_theta,max_theta) for _ in range(self.num_arms)]
            if not self.collision_checker(random_config):
               self.add_vertex(tuple(random_config))
        for v in self.graph:
            neighbors = self.find_K_nearest_neighbors(v, list(self.graph.keys()))
            for neighbor in neighbors:
                self.add_edge(neighbor, v)
    
    def query_path(self):               
        self.path_finding(self.start_config, self.end_config)
        
        
    def animation(self):
        self.animation = FuncAnimation(self.fig, self.update, frames = np.arange(0, 2 * np.pi, 0.01), blit=True, interval=50)            
        plt.show()
        
    def add_obstacle(self, coordinates):
        self.obstacles.append(Polygon(coordinates))
        
    def render_obstacles(self):
        for obstacle in self.obstacles:
            x, y = obstacle.exterior.xy
            self.ax.fill(x, y, alpha=0.6)
    
        
if __name__ == '__main__':
    # robot_2R = Robot(2, [2,1], [0, 1/4 *np.pi])
    # robot_2R.animation()
    start_config = [0, 1/4 * np.pi, 1/4 * np.pi]
    end_config = [-2/3 * np.pi, -1/2 * np.pi, -1.8/5 * np.pi]
    arm_length = [1,1,1.5]
    num_arm = 3
    
    robot_3R = Robot(num_arm, arm_length, start_config, end_config)
    robot_3R.add_obstacle([(2,-1), (3,1), (3,-2), (1,-3), (0,-1.5)])
    robot_3R.add_obstacle([(1,1), (1,3), (-1,3), (-1,0), (1,1)])
    robot_3R.render_obstacles()
    robot_3R.animation()
    
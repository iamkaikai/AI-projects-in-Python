import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import Polygon, LineString
from collections import deque


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
        self.end_line, = self.ax.plot([], [], 'bo-', lw=2, alpha = 0.2)
        self.ax.set_xlim(-sum(self.arm_lengths), sum(self.arm_lengths))
        self.ax.set_ylim(-sum(self.arm_lengths), sum(self.arm_lengths))
    
    def plot_end_config(self):
        x, y = self.kinematics(self.end_config)
        self.end_line.set_data(x, y)

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
        
    def interpolate_configurations(self, config1, config2, num_steps=200):
        interpolated_configs = []
        for step in range(1, num_steps + 1):
            interpolated_config = [t1 + step * (t2 - t1) / num_steps for t1, t2 in zip(config1, config2)]
            interpolated_configs.append(interpolated_config)
        return interpolated_configs

    def generate_interpolated_path(self):
        interpolated_path = [self.solution_path[0]]  # Start with initial configuration
        for i in range(len(self.solution_path) - 1):
            interpolated_path.extend(self.interpolate_configurations(self.solution_path[i], self.solution_path[i+1]))
        self.interpolated_solution_path = interpolated_path
    
    def update(self, frames):
        if frames < len(self.interpolated_solution_path):
            self.joints_angles = self.interpolated_solution_path[frames]
            x, y = self.kinematics(self.joints_angles)
            self.line.set_data(x, y)
            self.plot_end_config()
        return self.line, self.end_line
    
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
                    return True     # collision happens
        return False                # config is good
    
    def euclidean_distance(self, config1, config2):
        return np.linalg.norm(np.array(config2) - np.array(config1))           
    
    def find_K_nearest_neighbors(self, cur_vertex, all_vertices, k):
        dist = [(other_v, self.euclidean_distance(cur_vertex, other_v)) for other_v in all_vertices if other_v != cur_vertex]
        dist.sort(key = lambda pair: pair[1])
        return [vertex for vertex, dist in dist[:k]]
        
    def uniformal_search(self, graph, start, end):   
        unvisited_nodes = set([tuple(start)])
        visited_nodes = set()
        path = {}
        
        def trackPath(child, parent):
            path[child] = parent
            
        def reconstruct_path(cur_node):
            solution = [cur_node]
            while cur_node in path:
                cur_node = path[cur_node]
                solution.insert(0, cur_node)
            return solution
        
        while unvisited_nodes:
            cur_node = min(unvisited_nodes, key=lambda node: self.euclidean_distance(node, end))
            if cur_node == tuple(end):
                return reconstruct_path(cur_node)

            unvisited_nodes.remove(cur_node)
            visited_nodes.add(cur_node)
            
            for neighbor in graph[cur_node]:
                if neighbor in visited_nodes:
                    continue
                if neighbor not in unvisited_nodes:
                    unvisited_nodes.add(neighbor)                
                trackPath(neighbor, cur_node)
                
        return None
    
    def path_finding(self, start, end):
        path = self.uniformal_search(self.graph, start, end)
        if path:
            self.solution_path = path
            for p in path:
                x,y = self.kinematics(p)
                self.solution_line, = self.ax.plot([], [], 'ro-', lw=2, alpha = 0.03)
                self.solution_line.set_data(x, y)
            return path
        else:
            print("No solution found!!")
            return None
    
    def sampling_config(self, sample_size, k_size):
        min_theta = -np.pi
        max_theta = np.pi
        self.add_vertex(tuple(self.start_config))
        self.add_vertex(tuple(self.end_config))
        last_valid_config = tuple(self.start_config)
        
        def generate_random_config():
            return [np.random.uniform(min_theta,max_theta) for _ in range(self.num_arms)]
        
        for _ in range(sample_size):
            random_config = generate_random_config()
            
            while self.collision_checker(random_config):
                random_config = generate_random_config()
            
            interpolated_configs = self.interpolate_configurations(last_valid_config, random_config)
            collision_free_path = True
            
            for interpolated_config in interpolated_configs:
                if self.collision_checker(interpolated_config):
                    collision_free_path = False
                    break
            
            if collision_free_path:
                self.add_vertex(tuple(random_config))
                last_valid_config = random_config
            
        for v in self.graph:
            neighbors = self.find_K_nearest_neighbors(v, list(self.graph.keys()), k_size)
            for neighbor in neighbors:
                self.add_edge(neighbor, v)
    
    def query_path(self):               
        print(f'searching for path...')
        self.path_finding(self.start_config, self.end_config)
        
        
    def animation(self):
        if hasattr(self, 'solution_path'):
            self.generate_interpolated_path()
            num_frames = len(self.interpolated_solution_path)
            self.anim = FuncAnimation(self.fig, self.update, frames=num_frames, blit=True, interval=1)
            plt.show()
        else:
            print("No solution path to animate.")
        
    def add_obstacle(self, coordinates):
        self.obstacles.append(Polygon(coordinates))
        
    def render_obstacles(self):
        for obstacle in self.obstacles:
            x, y = obstacle.exterior.xy
            self.ax.fill(x, y, alpha=0.6)
    
        
if __name__ == '__main__':
    start_config = [0, 1/4 * np.pi, 1/4 * np.pi]
    end_config = [-2/3 * np.pi, -1/2 * np.pi, -1.8/5 * np.pi]
    arm_length = [1,1,1.5]
    num_arm = 3
    
    robot_3R = Robot(num_arm, arm_length, start_config, end_config)
    robot_3R.add_obstacle([(2,0), (3,1), (3,-2), (1,-3), (0,-1.5), (2,0)])
    robot_3R.add_obstacle([(1,1), (1,3), (-1,3), (-1,0), (1,1)])
    robot_3R.add_obstacle([(-1.5,2), (-1.5,-2), (-3,-3), (-3,2), (-1.5,2)])

    start_time = time.time()            # timing starts
    robot_3R.sampling_config(20000, 5)
    robot_3R.query_path()
    end_time = time.time()              # timing ends
    print(f"Function runtime: {end_time - start_time} seconds")
    
    robot_3R.render_obstacles()
    robot_3R.animation()
    
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import Polygon, LineString


class Robot:
    def __init__(self, num_arms, arm_lengths, joints_thetas):
        self.num_arms = num_arms
        self.arm_lengths = arm_lengths
        self.joints_angles = joints_thetas
        self.init_plot()
        self.obstacles = []
        self.joint_x = []
        self.joint_y = []
        
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
        self.line.set_data(x,y)
        self.joint_x = x
        self.joint_y = y
        
    def display(self):
        self.kinematics(self.joints_angles)
        plt.show()
        
    def update(self, frames):
        for i in range(len(self.joints_angles)):
            self.joints_angles[i] += 0.01 * np.pi
        self.kinematics(self.joints_angles)
        self.collision_checker()
        return self.line,
    
    def animation(self):
        self.animation = FuncAnimation(self.fig, self.update, frames = np.arange(0, 2 * np.pi, 0.01), blit=True, interval=50)            
        plt.show()
        
    def add_obstacle(self, coordinates):
        self.obstacles.append(Polygon(coordinates))
        
    def render_obstacles(self):
        for obstacle in self.obstacles:
            x, y = obstacle.exterior.xy
            self.ax.fill(x, y, alpha=0.6)
    
    def collision_checker(self):
        vertices = list(zip(self.joint_x, self.joint_y))
        self.arms = []
        for i in range(len(vertices)-1):
            self.arms.append(LineString([vertices[i], vertices[i+1]]))
        for arm in self.arms:
            for obstacle in self.obstacles:
                if arm.intersects(obstacle):
                    print(f'collision at {arm}')
        
if __name__ == '__main__':
    # robot_2R = Robot(2, [2,1], [0, 1/4 *np.pi])
    # robot_2R.animation()
    robot_3R = Robot(3, [2,1,1.5], [0, 1/4 *np.pi, 2/4 *np.pi])
    robot_3R.add_obstacle([(1,1), (2,2), (3,2), (1,-1), (1,1)])
    robot_3R.add_obstacle([(-3,-3), (-2,-2), (-1,-2), (-3,-1), (-3,-3)])
    robot_3R.render_obstacles()
    robot_3R.animation()
    
from shapely.geometry import Point, Polygon, LineString

# Define a simple robot as a point
robot = Point(0, 0)

# Define an obstacle as a polygon
obstacle = Polygon([(1, 1), (1, 3), (3, 3), (3, 1)])

# Define the robot's path as a line
path = LineString([(0, 0), (4, 4)])

# Check for collision
collision = path.intersects(obstacle)

print("Is there a collision?", collision)

# You can also check if the robot's current position is within the obstacle
in_obstacle = robot.within(obstacle)
print("Is the robot within the obstacle?", in_obstacle)

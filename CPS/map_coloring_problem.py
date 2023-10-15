from itertools import product
from backTracking import backTracking
import time

# define problem
class ConstraintSatisfactionProblem:
    def __init__(self, variables, domains, constraints, graph):
        self.variables = variables          # ['WA','NT','SA']
        self.domains = domains              # {'WA': ['R', 'G', 'B']...}
        self.constraints = constraints      # {('WA', 'NT'): [('R', 'B'), ...]}
        self.assignment = {}                # {'WA':'R', ....}
        self.neighbors = self.get_neighbors
    
    def get_neighbors(self, cur_variable):
        return graph.nodes[cur_variable]    # return a list
        
# create graph for map problem
class Graph:
    def __init__(self):
        self.nodes = {}
        
    def add_node(self, variable):
        if variable not in self.nodes:
            self.nodes[variable] = []
    
    def add_edge(self, node, neighbors):
        self.add_node(node)
        for neighbor in neighbors:
            self.nodes[node].append(neighbor)
            self.add_node(neighbor)
            self.nodes[neighbor].append(node)
            

graph = Graph()
graph.add_edge('WA',['NT','SA'])
graph.add_edge('NT',['WA','SA','Q'])
graph.add_edge('SA',['WA','NT','Q','NSW','V'])
graph.add_edge('Q',['NT','SA','NSW'])
graph.add_edge('NSW',['Q','SA','V'])
graph.add_edge('V',['SA','NSW'])
graph.add_node('T')
    
variables = list(graph.nodes.keys())
domains = {v: ['R', 'G', 'B'] for v in variables}
constraints = {}
assignment = {}

# generate all possible legal colors, BRUTE FORCE!!
for variable, neighbors in graph.nodes.items():
    for neighbor in neighbors:
        if (variable, neighbor) not in constraints and (neighbor, variable) not in constraints:
            legal_colors = [(c1,c2) for c1,c2 in product(domains[variable], domains[neighbor]) if c1 != c2]
            constraints[(variable,neighbor)] = legal_colors

csp = ConstraintSatisfactionProblem(variables, domains, constraints, graph)

solver = backTracking()

start_time = time.time()
solution = solver.back_tracking(assignment, csp)
end_time = time.time()

print('-------------------------')
print(solution)
print(f'brute force time = {end_time - start_time}')
print('-------------------------')

start_time = time.time()
solution = solver.back_tracking_ac3(assignment, csp)
end_time = time.time()

print('-------------------------')
print(solution)
print(f'inference time = {end_time - start_time}')
print('-------------------------')
from itertools import combinations, product
from backTracking import backTracking
from cps import ConstraintSatisfactionProblem

# define problem
# variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']

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

# generate all possible legal colors
for variable, neighbors in graph.nodes.items():
    for neighbor in neighbors:
        if (variable, neighbor) not in constraints and (neighbor, variable) not in constraints:
            legal_colors = [(c1,c2) for c1,c2 in product(domains[variable], domains[neighbor]) if c1 != c2]
            constraints[(variable,neighbor)] = legal_colors

csp = ConstraintSatisfactionProblem(variables, domains, constraints)
solver = backTracking()
solution = solver.back_tracking(assignment, csp)
print(solution)
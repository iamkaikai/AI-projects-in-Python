from backTracking import backTracking
import time

# define problem
class ConstraintSatisfactionProblem:
    def __init__(self, board, components):
        self.board = board                                              # an object
        self.components = components                                    # list of component ojbects
        self.variables = {component.id for component in components}     # {'a', 'b', ....}          
        self.domains = self.generate_domain()                           # {'a': [(0,0), (0,1)...], 'b':[(0,0), (0,1),...], ...}
        self.constraints = self.generate_constraints()
        self.gen_neighbors = self.generate_neighbors()
        self.neighbors = self.get_neighbors
        
        
        
    def generate_neighbors(self):
        neighbors = {variable: set() for variable in self.variables}
        for (var1, var2) in self.constraints.keys():
            neighbors[var1].add(var2)
            neighbors[var2].add(var1)
        return {var: list(neighbors_set) for var, neighbors_set in neighbors.items()}

    def get_neighbors(self, cur_variable):
        return self.neighbors[cur_variable]
    
    def get_neighbors(self, cur_variable):
        neighbors = set()
        for key in self.constraints:
            if cur_variable in key:
                neighbors.add(key[0] if key[1] == cur_variable else key[1])
        return list(neighbors)

        
    def generate_domain(self):
        domains = {}
        b_w = self.board.w
        b_h = self.board.h
        for component in self.components:
            c_w = component.w
            c_h = component.h
            domains[component.id] = [(x,y) for x in range(b_w - c_w + 1) for y in range(b_h - c_h + 1)]
        return domains
        

    def generate_constraints(self):
        constraints = {}
        for cur_component_idx, cur_component in enumerate(self.components):
            for other_component_idx, other_component in enumerate(self.components):
                if cur_component_idx != other_component_idx:
                    key = (cur_component.id, other_component.id)
                    legal_pos = []
                    for pos_cur in self.domains[cur_component.id]:
                        for pos_other in self.domains[other_component.id]:
                            cur_end_x = pos_cur[0] + cur_component.w
                            cur_end_y = pos_cur[1] + cur_component.h
                            other_end_x = pos_other[0] + other_component.w
                            other_end_y = pos_other[1] + other_component.h
                            
                            # Check for non-overlapping conditions
                            if (cur_end_x <= pos_other[0] or  
                                pos_cur[0] >= other_end_x or  
                                cur_end_y <= pos_other[1] or  
                                pos_cur[1] >= other_end_y):
                                legal_pos.append((pos_cur, pos_other))
                    constraints[key] = legal_pos
        return constraints

    
    def display(self, solution):
        canvas = [['⬛️' for _ in range(self.board.w)] for _ in range(self.board.h)]
        if solution != 'Solution not found!':
            for id, start_post in solution.items():
                component = next(c for c in self.components if c.id == id)
                start_x, start_y = start_post
                for dy in range(component.h):                
                    for dx in range(component.w):
                        canvas[start_y + dy][start_x + dx] = component.id
                        pass
            result = ''
            for row in reversed(canvas):
                result += ''.join(row) + '\n'
                
            return '\n' + result
        else:
            return 'no solution to display 😶'
class component:
    def __init__(self, id, width, height):
        self.w = width
        self.h = height
        self.id = id
        
class board:
    def __init__(self, w, h):
        self.w = w
        self.h = h


assignment = {}
board = board(10,10)
components = []
components.append(component('🟥', 3, 2))
components.append(component('🟧', 5, 2))
components.append(component('🟨', 2, 3))
components.append(component('🟩', 4, 6))
components.append(component('🟦', 5, 1))
components.append(component('🟪', 1, 7))
components.append(component('🟫', 3, 3))
components.append(component('🔷', 4, 3))
components.append(component('🟠', 3, 3))
components.append(component('🟢', 1, 3))
# components.append(component('🟡', 2, 3))


csp = ConstraintSatisfactionProblem(board, components)
solver = backTracking()
list_time = []
trials = 10000

for i in range(trials):
    start_time = time.time()
    solution = solver.back_tracking(assignment, csp)
    end_time = time.time()
    time_usage = end_time - start_time
    list_time.append(time_usage)

print('-------------------------')
print(solution)
print(csp.display(solution))
print(f'average time of backtracking in {trials} trials = {sum(list_time)/len(list_time)}')
print('-------------------------')


for i in range(trials):
    start_time = time.time()
    solution = solver.back_tracking_ac3(assignment, csp)
    end_time = time.time()
    time_usage = end_time - start_time
    list_time.append(time_usage)

print('-------------------------')
print(solution)
print(csp.display(solution))
print(f'average time of inference in {trials} trials = {sum(list_time)/len(list_time)}')
print('-------------------------')


from itertools import combinations, product
from backTracking import backTracking

class ConstraintSatisfactionProblem:
    def __init__(self, variables, domains, constraints):
        self.variables = variables          # ['WA','NT','SA']
        self.domains = domains              # {'WA': ['R', 'G', 'B']...}
        self.constrians = constraints       # {('WA', 'NT'): [('R', 'B'), ...]}
        self.assignment = {}                # {'WA':'R', ....}
        
    def check_constraint(c1, c2):
        return c1 != c2
        
    def is_complete(self, assignment):
        pass
    
    def get_unassigned_variables(self):
        pass
    
    def is_consistent(self, assignment):
        pass
    
    def back_tracking(self):
        
        # base case
        if self.is_complete(self.assignment):
            return self.assignment
        
        country_state = self.get_unassigned_variables()
        
        for color in self.domains[country_state]:
            if self.is_consistent(color, country_state):
                self.assignment[country_state] = color
                
                # recursion for rest of the 
                result = self.back_tracking()
                if result:
                    return result 
                else:
                    del self.assignment[country_state]
        
        # def backtrack(assignment, csp):
        # if is_complete(assignment, csp):
        #     return assignment
        # var = select_unassigned_variable(assignment, csp)
        # for value in domain_values(var, csp):
        #     if is_consistent(var, value, assignment, csp):
        #         assignment[var] = value
        #         result = backtrack(assignment, csp)
        #         if result:
        #             return result
        #         del assignment[var]
        # return None

        # def is_complete(assignment, csp):
        #     return set(assignment.keys()) == set(csp.variables)

        # def is_consistent(var, value, assignment, csp):
        #     # Implement consistency check
        #     pass

        # def select_unassigned_variable(assignment, csp):
        #     # Implement variable selection
        #     pass

        # def domain_values(var, csp):
        #     return csp.domains[var]




variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
domains = {v: ['R', 'G', 'B'] for v in variables}
constraints = {}

#generate all possible legal colors
for v1, v2 in combinations(variables,2):
    legal_colors = [(c1,c2) for c1,c2 in product(domains[v1], domains[v2]) if c1 != c2]
    constraints[(v1,v2)] = legal_colors


csp = ConstraintSatisfactionProblem(variables, domains, constraints)

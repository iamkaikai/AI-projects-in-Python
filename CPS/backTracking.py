class backTracking:          
 
    def check_constraint(c1, c2):
        return c1 != c2
        
    def is_complete(self, assignment, csp):
        return set(assignment.keys()) == set(csp.variables)
    
    def get_unassigned_variables(self, assignment, scp):
        for variable in scp.variables:
            if variable not in assignment:
                return variable
        return None
    
    def is_consistent(self, country_state, color, assignment, csp):
        for (v1, v2), legal_colors in csp.constraints.items():
            if country_state in [v1, v2]:
                the_other_state = v2 if country_state == v1 else v1
                if the_other_state in assignment:
                    c1, c2 = color, assignment[the_other_state]
                    if (c1, c2) not in legal_colors and (c2, c1) not in legal_colors:
                        return False
        return True
    
    def back_tracking(self, assignment, csp):
        # base case
        if self.is_complete(assignment, csp):
            return assignment
        
        # select a variable from csp
        country_state = self.get_unassigned_variables(assignment, csp)
        
        # check all colors in the domain
        for color in csp.domains[country_state]:
            if self.is_consistent(country_state, color, assignment, csp):
                assignment[country_state] = color
                result = self.back_tracking(assignment, csp)
                if result:
                    return result 
                else:
                    del assignment[country_state]
        return 'Solution not found!'


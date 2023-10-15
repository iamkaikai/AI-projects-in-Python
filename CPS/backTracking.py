from AC3 import AC3
import copy

class backTracking:
    def is_complete(self, assignment, csp):
        return set(assignment.keys()) == set(csp.variables)

    def get_unassigned_variables(self, assignment, csp):
        for variable in csp.variables:
            if variable not in assignment:
                return variable
        return None

    def is_consistent(self, component, value, assignment, csp):
        for other_component, other_value in assignment.items():
            key = (component, other_component)
            if key in csp.constraints and (value, other_value) not in csp.constraints[key]:
                return False
        return True


    def back_tracking(self, assignment, csp):
        
        if self.is_complete(assignment, csp):       # base case to stop recursion
            return assignment

        variable = self.get_unassigned_variables(assignment, csp)
        if variable is None:
            return 'Solution not found!'

        for value in csp.domains[variable]:
            if self.is_consistent(variable, value, assignment, csp):
                assignment[variable] = value
                result = self.back_tracking(assignment, csp)
                if result != 'Solution not found!':
                    return result
                del assignment[variable]

        return 'Solution not found!'
    
    
    def back_tracking_ac3(self, assignment, csp):
        ac3 = AC3(csp)
    
        if not ac3.inference():
            return 'Solution not found!'

        if self.is_complete(assignment, csp):
            return assignment

        variable = self.get_unassigned_variables(assignment, csp)
        if variable is None:
            return 'Solution not found!'

        for value in csp.domains[variable]:
            if self.is_consistent(variable, value, assignment, csp):
                assignment[variable] = value
                result = self.back_tracking(assignment, csp)
                if result != 'Solution not found!':
                    return result
                del assignment[variable]

        return 'Solution not found!'

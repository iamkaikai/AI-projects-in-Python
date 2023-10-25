from Sudoku import Sudoku
import random

class SAT:
    def __init__(self, file, load_cnf = False):
        self.file = file                    # puzzle file
        if self.file:                       # initiate sudoku
            self.sudoku = Sudoku()          # create sudoku object
            self.sudoku.load(file)          # e.g. "puzzle.sud"
        if load_cnf:
            self.sudoku.generate_cnf(file[:-4] + ".cnf")    # generate .cnf by using the same name of sudoku
        else:
            self.load_Clauses(file[:-4] + ".cnf")
    
    def load_Clauses(self, file):
        self.clauses = []
        self.variables = set()
        self.cnf =  open(file, "r")
        for line in self.cnf:
            line = line.strip()             # clean format
            literals = list(map(int, line.split()))
            self.variables.update(abs(v) for v in literals)
            self.clauses.append(literals)
            
    def check_clauses(self, CNF, assignment):
        for clause in CNF:
            satisfaction = False
            for literal in clause:
                if literal > 0:
                    if assignment[literal] is True:
                        satisfaction  = True
                        break
                else:
                    if assignment[abs(literal)] is False:
                        satisfaction  = True
                        break
            if not satisfaction:
                return False
        return True           
    
    def write_solution(self, assignment, output_path):
        print(f'assignment of the solution = {assignment}')
        with open(output_path, "w") as f:
            for variable, value in assignment.items():
                if value is True:
                    f.write(str(variable) + '\n')
                    
        
    def GSAT(self, threshold = 0.2, max_iter = 100000):
        print(f'solving problem...\nmax search: {max_iter}\n')
        count = 0
        best_score_repeat_count = 0
        list_variables = list(self.variables)
        
        # randomly initialized starting assignment
        assignment = {}
        for variable in self.variables:
            assignment[variable] = random.choice([True, False])
        
        while count < max_iter:
            print(f'iteration {count}...')
                
            if self.check_clauses(self.clauses, assignment):
                print('solution found!!!')
                return assignment
            
            # randomly negate one variable in the assignment
            if random.random() < threshold:
                selected_var = random.choice(list_variables)
                assignment[selected_var] = not assignment[selected_var]
            else:
                score = {}
                prev_best = None
                for var in self.variables:
                    assignment[var] = not assignment[var]
                    score[var] = sum(self.check_clauses([clause], assignment) for clause in self.clauses)
                    assignment[var] = not assignment[var]
                    
                best_score = max(score.values())
                prev_best = best_score
                best_flip = [var for var, s in score.items() if s == best_score]
                print(f'satisfied clauses = {best_score}/{len(self.clauses)}; len of [best_flip] = {len(best_flip)}\n')

                # randomly flip a variable when choosing the best variable to avoid local minimun                
                if random.random() < threshold:      
                   selected_var = random.choice(list_variables)  # random flip
                else:
                    if prev_best == best_score:
                        best_score_repeat_count += 1
                    selected_var = random.choice(best_flip)
                    
                assignment[selected_var] = not assignment[selected_var]
                
                # if the search is stuck at local minimun at 99% of completion, 
                # flip 10 random variables when the best score repeat 10 times
                if best_score_repeat_count > 10 and best_score/len(self.clauses) > 0.99:
                    # threshold = 0.1
                    for _ in range(20):
                        selected_var = random.choice(list_variables)
                        assignment[selected_var] = not assignment[selected_var]
                    best_score_repeat_count = 0
            
            count += 1
        
        return None
    
    def walkSAT(self, threshold = 0.3, max_iter = 100000):
        print(f'solving problem...\nmax search: {max_iter}\n')
        count = 0
        
        assignment = {}
        for variable in self.variables:
            assignment[variable] = random.choice([True, False])
            
        while count < max_iter:
            print(f'iteration {count}...')
            
            if self.check_clauses(self.clauses, assignment):
                print('solution found!!!')
                return assignment
            
            unsatisfied_clauses = [clause for clause in self.clauses if not self.check_clauses([clause], assignment)]
            random_clause = random.choice(unsatisfied_clauses)
            
            if random.random() < threshold:
                selected_var = random.choice([abs(var) for var in random_clause])
            else:
                score = {}
                for var in random_clause:
                    abs_var = abs(var)
                    assignment[abs_var] = not assignment[abs_var]
                    score[abs_var] = sum(self.check_clauses([clause], assignment) for clause in self.clauses)
                    assignment[abs_var] = not assignment[abs_var]
                    
                best_score = max(score.values())
                best_flip = [var for var, s in score.items() if s == best_score]
                selected_var = random.choice(best_flip)
                print(f'best_score = {best_score}/{len(self.clauses)}; len of [best_flip] = {len(best_flip)}\n')
                
            assignment[selected_var] = not assignment[selected_var]            
            count += 1
            
        return None
    
   
   
    ############################ Bonus ############################
    # try to implement the algo bases on the pseudo code below:
    # https://en.wikipedia.org/wiki/DPLL_algorithm
        
    def unit_propagate(self, l, clauses, assignment):
        assignment[l] = True  # Assign true to the literal
        new_clauses = []  # Initialize a new clause list

        for clause in clauses:
            if l in clause:
                continue  
            
            new_clause = [x for x in clause if x != -l]  
            if len(new_clause) == 0:
                return None, None  
            
            if l in assignment and assignment[l] == False:
                return None, None
            
            new_clauses.append(new_clause)  

        return new_clauses, assignment  


    def pure_literal_assign(self, l, clauses, assignment):
        assignment[l] = True  
        new_clauses = []  
        
        for clause in clauses:
            if l not in clause and -l not in clause:
                new_clauses.append(clause)  
            
            if l in assignment and assignment[l] == False:
                return None, None

        return new_clauses, assignment 


    def DPLL(self, clauses, assignment={}, count = 0):
        print(f'count = {count}')
        
        # Unit propagation
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            unit = unit_clauses.pop(0)
            clauses, assignment = self.unit_propagate(unit[0], clauses, assignment)
            if clauses is None:
                return False, {}
                    
        # Pure literal elimination
        all_literals = [lit for clause in clauses for lit in clause]
        pure_literals = set(l for l in all_literals if -l not in all_literals)
        for l in pure_literals:
            clauses, assignment = self.pure_literal_assign(l, clauses, assignment)
            if clauses is None:
                return False, {}

        # Check for stopping conditions
        if not clauses:
            return True, assignment
        for clause in clauses:
            if not clause:
                return False, {}
        
        # Recursive DPLL
        l = random.choice(all_literals)
        
        # Try assigning False to l
        new_assignment = assignment.copy()
        new_assignment[l] = False
        new_clauses = [[x for x in clause if x != -l] for clause in clauses if l not in clause]
        sat, new_assignment = self.DPLL(new_clauses, new_assignment, count + 1)
        if sat:
            return True, new_assignment
        
        # Restore the original clauses for the next recursive call
        clauses = [clause[:] for clause in clauses]

        # Try assigning True to l
        new_assignment = assignment.copy()
        new_assignment[l] = True
        new_clauses = [[x for x in clause if x != l] for clause in clauses if -l not in clause]
        sat, new_assignment = self.DPLL(new_clauses, new_assignment, count + 1)
        if sat:
            return True, new_assignment

        return False, {}

    def DPLL_SAT(self):
        sat, assignment = self.DPLL(self.clauses)
        if sat:
            print("Satisfiable, assignment:", assignment)
        else:
            print("Unsatisfiable")

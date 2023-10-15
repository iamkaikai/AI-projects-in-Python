class AC3:          
    def __init__(self, csp):
        self.constraints = csp.constraints
        self.domains = csp.domains
        self.neighbors = csp.neighbors      # a function to get neighbors in the input object
        
    
    def need_modification(self, xi, xj):
        modified = False
        for color_xi in self.domains[xi]:            
            satisfaction = False
            for color_xj in self.domains[xj]:
                if (color_xi , color_xj) in self.constraints.get((xi, xj)):
                    satisfaction = True
                    break
            if not satisfaction:
                self.domains[xi].remove(color_xi)
                modified = True
        return modified
    
    def inference(self):
        q = list(self.constraints.keys())
        while q:
            xi, xj = q.pop(0)
            if self.need_modification(xi, xj):
                if not self.domains[xi]:                # if domain of xi is empty, meaning not satisfiable
                    return False
                for neighbor in self.neighbors(xi):         # add neighbors to the queue
                    if neighbor != xj:                  # prevent infinite loop
                        q.append((neighbor,xi))
        return True        
        
        
    
class ConstraintSatisfactionProblem:
    def __init__(self, variables, domains, constraints):
        self.variables = variables          # ['WA','NT','SA']
        self.domains = domains              # {'WA': ['R', 'G', 'B']...}
        self.constraints = constraints       # {('WA', 'NT'): [('R', 'B'), ...]}
        self.assignment = {}                # {'WA':'R', ....}
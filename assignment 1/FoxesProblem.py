class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        # you might want to add other things to the problem,
        # like the total number of chickens (which you can figure out
        # based on start_state

    # helper function to check whether the state is legal
    # check whether either side of the num of foxes is greater than chicken
    def check(self, state):
        opposite_state = tuple(a - b for a, b in zip(self.start_state, state))
        if (state[0] < state[1] and state[0]>0) or (opposite_state[0] < opposite_state[1] and opposite_state[0]>0):
            return False
        
        if any(s < 0 for s in state) or any(s < 0 for s in opposite_state):
            return False

        return True

    # get successor states for the given state
    def get_successors(self, state):
        # you write this part. I also had a helper function
        # that tested if states were safe before adding to successor list
        successors = []
        chicken, fox, boat = state
        multiplier = -1 if boat else 1
        actions = [(1, 0), (0,1), (1,1), (2,0), (0,2)]    
        successors = [(chicken + a * multiplier, fox + b * multiplier, boat + multiplier) for a, b in actions]
        legal_successors = [s for s in successors if self.check(s)]
        return legal_successors
    
    
    # I also had a goal test method. You should write one.
    def goal_check(self, state):
        if state == self.goal_state:
            return True

    # reform the printing format
    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string


## A bit of test code
if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    # print(test_cp)

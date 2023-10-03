from MinimaxAI import MinimaxAI

class MinimaxAI():
    def __init__(self, max_depth):
        self.max_depth = max_depth
    
    def iterative_minimax(self, max_depth):
        for i in range(max_depth):
            MinimaxAI(i)
        
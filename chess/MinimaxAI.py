import chess
import random

class MinimaxAI():
    def __init__(self, depth):
        self.depth = depth      # max depth
        self.visited_noeds = 0

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    # I use material value for my heuristic
    def evalute_move(self, board):
        if board.is_checkmate():
            return float('inf') if board.turn else -float('inf')
        ev = 0
        values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 25,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -25
        }
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            piece_value = values.get(str(piece))
            if piece and piece_value:
                ev += piece_value
                
        # return ev + random.uniform(0, 0.01)     # adding random value to avoid looping behavior, REF: https://stackoverflow.com/questions/69372792/chess-programming-minimax-detecting-repeats-transposition-tables
        return ev
    
    
    def minimax(self, board, depth, maxPlayer):
        self.visited_noeds +=1
                
        # base case
        if self.cutoff_test(board, depth):
            return self.evalute_move(board)
        
        # swith between min and max fn
        if maxPlayer:
            maxEV = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, False)
                maxEV = max(maxEV, eval)
                board.pop()
            return maxEV
        else:
            minEV = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, True)
                minEV = min(minEV, eval)
                board.pop()
            return minEV
        
        
    def choose_move(self, board):
        best_move = None
        best_ev = -float('inf')
        
        for move in board.legal_moves:
            board.push(move)
            ev = self.minimax(board, self.depth, True)
            board.pop()
            if ev > best_ev:
                best_move = move
                best_ev = ev
        print("Minimax AI recommending move " + str(best_move))        
        print(f"visited nodes = {self.visited_noeds}")
        print('-------------------------------')
        return best_move
            

        


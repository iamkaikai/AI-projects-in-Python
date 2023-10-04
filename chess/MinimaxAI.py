import chess
import random
from evalute_move import evalute_move

class MinimaxAI():
    def __init__(self, depth):
        self.depth = depth      # max depth
        self.visited_noeds = 0

    def cutoff_test(self, board, depth):
        if board.is_game_over():
            return True

        if board.is_stalemate():
            return True

        if board.can_claim_fifty_moves():
            return True
        
        return depth == 0    
    
    def minimax(self, board, depth, maxPlayer):
        self.visited_noeds +=1
                
        # base case
        if self.cutoff_test(board, depth):
            return evalute_move(board, depth)
        
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
            

        


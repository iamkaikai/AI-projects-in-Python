import chess
import random

class MinimaxAI_iterative():
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
    
    def evalute_board(self, board):
        total = 0
       
        opponent_piece_count = 1
        values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -100
        }
        
        if board.is_game_over():
            result = board.result()
            if result == '1-0':
                return 5000
            elif result == '0-1':
                return -5000
            else:
                return 0
            
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            piece_value = values.get(str(piece))
            if piece and piece_value:
                total += piece_value
                
            # count the num of enemy's pieces
            if board.piece_at(square) and board.piece_at(square).color != board.turn:
                opponent_piece_count +=1
            
        total -= opponent_piece_count + random.random()*0.01
        return total
    
    def minimax(self, board, depth, maxPlayer):
        self.visited_noeds +=1
                
        # base case
        if self.cutoff_test(board, depth):
            return self.evalute_board(board)
        
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
        best_move_global = None
        
        # make it turn dependant
        if board.turn:  
            best_ev_global = -float('inf')
        else:
            best_ev_global = float('inf')
            
        for depth in range(1, self.depth+1):
            best_move = None
            if board.turn:  
                best_ev = -float('inf')
                isMaximizing = True
            else:
                best_ev = float('inf')
                isMaximizing = False
            for move in board.legal_moves:
                board.push(move)
                ev = self.minimax(board, depth, isMaximizing)
                board.pop()
                
                if (isMaximizing and ev > best_ev) or (not isMaximizing and ev < best_ev):
                    best_move = move
                    best_ev = ev
                    
                if (isMaximizing and best_ev > best_ev_global) or (not isMaximizing and best_ev < best_ev_global):
                    best_move_global = best_move
                    best_ev_global = best_ev
                    
        print("Minimax AI recommending move " + str(best_move))        
        print(f"visited nodes = {self.visited_noeds}")
        print('-------------------------------')
        return best_move_global
            

        


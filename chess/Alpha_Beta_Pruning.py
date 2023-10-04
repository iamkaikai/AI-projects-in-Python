import chess
import random
from evalute_move import evalute_move

class A_B_Pruning():
    def __init__(self, depth):
        self.depth = depth      # max depth
        self.visited_nodes = 0
        self.transposition_table = {}

    def cutoff_test(self, board, depth):
        if board.is_game_over():
            return True

        if board.is_stalemate():
            return True

        if board.can_claim_fifty_moves():
            return True
        
        return depth == 0
    
    def board_hash(self, board):
            return hash(str(board))
        
    def minimax(self, board, depth, alpha, beta, maxPlayer):
        self.visited_nodes +=1
        board_key = self.board_hash(board)
        
        # if seen the move before with same ev, skip search
        if board_key in self.transposition_table:
            stored_depth, stored_value = self.transposition_table[board_key]
            if stored_depth <= depth:
                return stored_value
        
        # base case
        if self.cutoff_test(board, depth):
            return evalute_move(board, depth)
        
        # Null-move heuristic
        # if depth >= 2 and not board.is_check():
        #     board.push(chess.Move.null())
        #     null_score = -self.minimax(board, depth - 1 - 2, -beta, -beta + 1, not maxPlayer)
        #     board.pop()
        #     if null_score >= beta:
        #         return beta
        
        if maxPlayer:
            maxEV = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, False)
                board.pop()
                maxEV = max(maxEV, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = (depth, maxEV)
            return maxEV
        else:
            minEV = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, True)
                board.pop()
                minEV = min(minEV, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = (depth, minEV)
            return minEV
        
    def choose_move(self, board):
        best_move = None
        best_ev = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        
        for move in board.legal_moves:
            board.push(move)
            ev = self.minimax(board, self.depth, alpha, beta, True)
            board.pop()
            if ev > best_ev:
                best_move = move
                best_ev = ev
            alpha = max(alpha, ev)
        print("Alpha-Beta Pruning AI recommending move " + str(best_move))        
        print(f"visited nodes = {self.visited_nodes}")
        print(f'best_ev = {best_ev}')
        print('-------------------------------')
        return best_move
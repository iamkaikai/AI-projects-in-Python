import chess
import random
from evalute_move import evalute_board, evaluate_sort

class A_B_Pruning():
    def __init__(self, depth):
        self.depth = depth      # max depth
        self.visited_nodes = 0
        self.transposition_table = {}
        
        #Zobrist hash ref: https://en.wikipedia.org/wiki/Zobrist_hashing#:~:text=Zobrist%20hashing%20(also%20referred%20to,used%20to%20avoid%20analyzing%20the
        self.zobrist_table = {}         
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
        for piece in pieces:
            self.zobrist_table[piece] = {}
            for sq in range(64):
                self.zobrist_table[piece][sq] = random.getrandbits(64)

    def cutoff_test(self, board, depth):
        if board.is_game_over():
            return True

        if board.is_stalemate():
            return True

        if board.can_claim_fifty_moves():
            return True
        
        if depth == 0:
            return True
    
    # basic python biult-in hashing fn
    # def board_hash(self, board):
    #         return hash(str(board))
        
    def zobrist_hash(self, board):
        hash = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece = str(piece)
                hash ^= self.zobrist_table[piece][square]
        return hash

        
    def minimax(self, board, depth, alpha, beta, maximizing):
        self.visited_nodes +=1
        board_key = self.zobrist_hash(board)
        
        # if seen the move before with same ev, skip search
        if board_key in self.transposition_table:
            stored_value = self.transposition_table[board_key]
            return stored_value
            
        # base case
        if self.cutoff_test(board, depth):
            return evalute_board(board, self.transposition_table)
        
        # sorting moving orders to improve seraching speed
        legal_moves = list(board.legal_moves)
        sorted_moves = sorted(legal_moves, key=lambda move: evaluate_sort(board, move, self.transposition_table), reverse=True)
            
        if maximizing:
            bestEval = -float('inf')
            for move in sorted_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, False)
                board.pop()
                bestEval = max(bestEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        else:
            bestEval = float('inf')
            for move in sorted_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, True)
                board.pop()
                bestEval = min(bestEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                
        self.transposition_table[board_key] = bestEval    
        return bestEval
        
    def choose_move(self, board):
        self.visited_nodes = 0
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
        print('-----------------------------------------------')
        return best_move
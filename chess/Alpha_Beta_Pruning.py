import chess
import random

class A_B_Pruning():
    def __init__(self, depth):
        self.depth = depth      # max depth
        self.visited_nodes = 0
        self.transposition_table = {}

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    def board_hash(self, board):
            return hash(str(board))
        
    # I use material value for my heuristic
    def evalute_move(self, board, depth):
        pieces_value = 0
        values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -100
        }
        # sum up all the pieces for total ev
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            piece_value = values.get(str(piece))
            if piece and piece_value:
                pieces_value += piece_value        
                
        # the more possible moves the better
        num_moves = len(list(board.legal_moves))
        
        # penalize going depper
        depth_score = depth*2
        
        return pieces_value + num_moves + depth_score
    
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
            return self.evalute_move(board, depth)
        
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

                

        


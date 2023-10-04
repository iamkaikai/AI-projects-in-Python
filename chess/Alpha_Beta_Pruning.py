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
        
        if  board.is_repetition(3) or board.can_claim_threefold_repetition():
            return True
    
        if depth == 0:
            return True
    
    def board_hash(self, board):
            return hash(str(board))
        
    def evaluate_move_score(self, board, move):
        score = 0
        if board.is_capture(move):
            piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000}
            
            if board.piece_at(move.to_square):
                captured_piece = board.piece_at(move.to_square).symbol().upper()
                captured_value = piece_values.get(captured_piece)
                capturing_piece = board.piece_at(move.from_square).symbol().upper()
                capturing_value = piece_values.get(capturing_piece)    
                if captured_piece and captured_value:
                    score += captured_value*10
                if captured_value and capturing_value:
                    score += 10 * (captured_value - 0.5 * capturing_value)
            
        board.push(move)
        score += 0.1 * board.legal_moves.count() ** 0.5
        board.pop()
        
        board.push(move)
        if board.is_checkmate():
            score += 1000
        elif board.is_check():
            score += 500
        board.pop()

        return score

        
    def minimax(self, board, depth, alpha, beta, maxPlayer):
        self.visited_nodes +=1
        board_key = self.board_hash(board)
        
        # if seen the move before with same ev, skip search
        if board_key in self.transposition_table:
            stored_value = self.transposition_table[board_key]
            return stored_value
        
        # base case
        if self.cutoff_test(board, depth):
            return evalute_move(board)
        
        legal_moves = list(board.legal_moves)
        sorted_moves = sorted(legal_moves, key=lambda move: self.evaluate_move_score(board, move), reverse=True)
            
        if maxPlayer:
            maxEV = -float('inf')
            for move in sorted_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, False)
                board.pop()
                maxEV = max(maxEV, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = maxEV
            return maxEV
        else:
            minEV = float('inf')
            for move in sorted_moves:
                board.push(move)
                eval = self.minimax(board, depth-1, alpha, beta, True)
                board.pop()
                minEV = min(minEV, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = minEV
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
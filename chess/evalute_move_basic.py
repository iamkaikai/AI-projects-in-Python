import chess
import random

class evaluation:
    def __init__(self, zobrist_table):
        self.zobrist_table = zobrist_table
    
    def zobrist_hash(self, board):
            hash = 0
            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece:
                    piece = str(piece)
                    hash ^= self.zobrist_table[piece][square]
            return hash

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

    def evaluate_sort(self, board, move):
            score = 0
            board.push(move)
            score += self.evalute_board(board)
            score += 0.1 * (board.legal_moves.count() ** 0.5)
            board.pop()
            return score

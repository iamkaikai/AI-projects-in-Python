import chess
import random

# this evaluation is not turn dependat, it only works as player1
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

    def evalute_board(self, board, transposition_table):
        total = 0
        opponent_king_square = board.king(not board.turn)
        opponent_piece_count = 1
        endgame_threshold = 4
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
        
        board_key = self.zobrist_hash(board)
        if board_key in transposition_table:
            return transposition_table[board_key]
            
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            piece_value = values.get(str(piece)) 
            if piece and piece_value:
                total += piece_value
            
            # count the num of enemy's pieces to check end game threshold
            if board.piece_at(square) and board.piece_at(square).color != board.turn:
                opponent_piece_count +=1
            
        #end game strategy
        if opponent_piece_count <= endgame_threshold and board.turn:
            board.push(chess.Move.null())
            opponent_legal_moves_count = board.legal_moves.count()
            board.pop()
            total -= opponent_piece_count    
            if opponent_legal_moves_count > 0 and board.turn:  
                total -= opponent_legal_moves_count 
            
            # Reward moves that restrict the opponent's king's mobility
            distance_to_opponent_king = chess.square_distance(square, opponent_king_square)
            if 4 > opponent_piece_count > 0:
                total -= (distance_to_opponent_king / opponent_piece_count)*0.5
                
        total -= opponent_piece_count + random.random()*0.01
        # transposition_table[board_key] = total
        return total

    def evaluate_sort(self, board, move, depth, transposition_table, total_step):
            score = 0
            
            # Reward for taking center of the board
            center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
            if move in center_squares:
                score += 1 if board.turn else -1
                
            board.push(move)
            score += self.evalute_board(board, transposition_table)
            score += 0.1 * (board.legal_moves.count() ** 0.5)
            board.pop()
            return score

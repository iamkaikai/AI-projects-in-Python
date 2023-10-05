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

    def evalute_board(self, board, depth, transposition_table, total_step):
        total = 0
        opponent_king_square = board.king(not board.turn)
        my_king_square = board.king(board.turn)
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
        # if board_key in transposition_table:
        #     stored_value, stored_depth = transposition_table[board_key]
        #     if depth > stored_depth:
        #         return stored_value
            
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            piece_value = values.get(str(piece))
            
            # count the num of enemy's pieces
            if board.piece_at(square) and board.piece_at(square).color != board.turn:
                opponent_piece_count +=1
            
            # Sum up all the pieces' values and check for penalties or rewards for being attacked or attacking
            if piece and piece_value:
                total += piece_value
                
                # Penalize if our pieces are under attack
                if piece.color == board.turn and board.is_attacked_by(not board.turn, square):
                    total -= abs(piece_value) * 3  
                    
                # Reward if we are attacking opponent's pieces
                # elif piece.color != board.turn and board.is_attacked_by(board.turn, square):
                #     total += abs(piece_value) 
            
        # distance_to_opponent_king = chess.square_distance(square, opponent_king_square)
        # if opponent_piece_count > 0:
        #     total -= (distance_to_opponent_king / opponent_piece_count)*0.1
            
                
        #end game strategy
        # if opponent_piece_count <= endgame_threshold and board.turn:
        #     board.push(chess.Move.null())
        #     opponent_legal_moves_count = board.legal_moves.count()
        #     board.pop()
        #     total -= opponent_piece_count*200    
        #     if opponent_legal_moves_count > 0 and board.turn:  
        #         total += 800/opponent_legal_moves_count 
            
        #     # Reward moves that restrict the opponent's king's mobility
        #     if opponent_piece_count > 0:
        #         total -= (distance_to_opponent_king / opponent_piece_count)*0.5
            
                
        # legal_moves = list(board.legal_moves)        
        # for move in legal_moves:
        #     # Count the opponent's legal moves. Reward based on restricting the opponent's legal moves
        #     center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        #     if move in center_squares:
        #         score += 1 if board.turn else -1
            
        #     # Reward for attacking opponent's king
        #     if board.is_attacked_by(board.turn, opponent_king_square):
        #         total += 100
                
        #     if board.is_attacked_by(board.turn, my_king_square):
        #         total -= 250

        #     capturing_piece = board.piece_at(move.from_square)
        #     target_piece = board.piece_at(move.to_square)
            
        #     if target_piece:  # Add this check
        #         target_value = values[str(target_piece)]
            
        #     if board.is_capture(move) and capturing_piece and target_piece:
        #         total += target_value if board.turn else -target_value
                
        total -= opponent_piece_count + random.random()*0.01
        # transposition_table[board_key] = (total, depth)
        return total

    def evaluate_sort(self, board, move, depth, transposition_table, total_step):
            score = 0
            board.push(move)
            score += self.evalute_board(board, depth, transposition_table, total_step)
            score += 0.1 * (board.legal_moves.count() ** 0.5)
            board.pop()
            return score

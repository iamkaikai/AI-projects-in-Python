import chess

def evalute_move(board, depth):
        if board.is_checkmate():
            return float('inf') if board.turn else -float('inf')
        
       
        values = {
            'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
            'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000
        }
        
        piece_weights = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9}
        
        # sum up all the pieces for total ev
        total_pieces_value = 0
        defense_penalty = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            piece_value = values.get(str(piece))
            if piece and piece_value:
                total_pieces_value += piece_value
                
                # penalty for being attacked    
                if board.is_attacked_by(not board.turn, square):
                        defense_penalty -= abs(piece_value)
                    
        # Check if the piece can capture an enemy piece
        capture_bonus = 0
        mobility_bonus = 0
        legal_moves = list(board.legal_moves)        
        for move in legal_moves:
            if board.is_capture(move):
                capturing_piece = board.piece_at(move.from_square)
                target_piece = board.piece_at(move.to_square)
                if capturing_piece and target_piece:
                    capture_bonus += abs(values[str(target_piece)]) - abs(values[str(capturing_piece)])
                
            moving_piece = board.piece_at(move.from_square)
            moving_value = piece_weights.get(str(moving_piece))
            if moving_piece and moving_value:
                mobility_bonus += moving_value
            
        return total_pieces_value + capture_bonus + defense_penalty + mobility_bonus
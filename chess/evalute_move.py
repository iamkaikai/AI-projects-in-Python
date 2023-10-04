import chess

def evalute_move(board):
    total = 0
    if board.is_checkmate():
        return float('inf') if board.turn else -float('inf')
    
    if board.is_repetition(3) or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves() or board.is_fifty_moves():
        total -= 999
    
    values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000
    }
    
    piece_weights = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9}
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        piece_value = values.get(str(piece))
        if piece and piece_value:
            total += piece_value
            if board.is_attacked_by(not board.turn, square):
                total -= abs(piece_value)
                
    legal_moves = list(board.legal_moves)        
    for move in legal_moves:
        if board.is_capture(move):
            capturing_piece = board.piece_at(move.from_square)
            target_piece = board.piece_at(move.to_square)
            if capturing_piece and target_piece:
                total += abs(values[str(target_piece)]) - abs(values[str(capturing_piece)]) * 0.5
                
        moving_piece = board.piece_at(move.from_square)
        moving_value = piece_weights.get(str(moving_piece))
        if moving_piece and moving_value:
            total += moving_value
    
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    if move.to_square in center_squares:
        total += 0.5

    return total

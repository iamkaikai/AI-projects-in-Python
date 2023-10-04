import chess

def evalute_board(board, transposition_table):
    total = 0
    opponent_king_square = board.king(not board.turn)
    
    if board.is_checkmate():
        return float('inf') if board.turn else -float('inf')
    
    board_key = hash(str(board))
    if board_key in transposition_table:
        return transposition_table[board_key]
    
    values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000
    }
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        piece_value = values.get(str(piece))
        
        # sum up all the pieces values and check penalty for being attack
        if piece and piece_value:
            total += piece_value
            if board.is_attacked_by(not board.turn, square):
                total -= abs(piece_value)*2
                
        # Reward moves that restrict the opponent's king's mobility
        if piece and piece.color == board.turn:
            distance_to_opponent_king = chess.square_distance(square, opponent_king_square)
            total -= distance_to_opponent_king
            if board.is_attacked_by(board.turn, opponent_king_square):
                total += 75
        
                
    legal_moves = list(board.legal_moves)        
    for move in legal_moves:
        capturing_piece = board.piece_at(move.from_square)
        target_piece = board.piece_at(move.to_square)
        
        if target_piece:  # Add this check
            target_value = values[str(target_piece)]
        
        if board.is_capture(move) and capturing_piece and target_piece:
            total += target_value if board.turn else -target_value

    # Zugzwang
    if len(legal_moves) < 3:  # Adjust the number as you see fit
        total -= 50
    
    # Piece Coordination
    if board.is_attacked_by(board.turn, opponent_king_square):
        total += 30
    
    # 50-Move Counter
    if board.halfmove_clock >= 90:
        total -= 100

    return total

def evaluate_sort(board, move, transposition_table):
        score = 0
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        
        board_key = hash(str(board))
        if board_key in transposition_table:
            return transposition_table[board_key]
        
        if move in center_squares:
            total += 1 if board.turn else -1
            
        #check for mobility and penalty for repetition
        board.push(move)
        if board.is_repetition(5) or board.can_claim_threefold_repetition() or board.can_claim_fifty_moves() or board.is_fifty_moves():
            score -= 100
        if board.is_checkmate():
            score += 1000 if board.turn else -1000
        if board.is_check():
            score += 50 if board.turn else -50
        score += 0.1 * (board.legal_moves.count() ** 0.5)
        board.pop()
        
        if board.halfmove_clock >= 90:
            score -= 100
        
        return score

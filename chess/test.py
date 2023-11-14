import chess

board = chess.Board()
for square in chess.SQUARES:
    piece = board.piece_at(square)
    print(piece)
    print(type(piece))
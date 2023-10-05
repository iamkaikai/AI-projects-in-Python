import chess

class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        # self.board.set_fen("2k5/8/4p3/2P2Q2/5P2/4R1K1/4P1P1/2R1B3 w - - 0 1")
        # self.board.set_fen("rnbqkbn1/2pp1ppr/7p/p1p1p1p1/8/4PPKP/PPP1P3/RNBQ1BNR b - - 0 1")
        # self.board.set_fen("7k/4N3/p3p3/8/7p/P4P1P/P1PPPKP1/R1BQ1BNR w - - 0 1")
        self.players = [player1, player2]

    def make_move(self):
        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)
        self.board.push(move)  # Make the move
        
    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"

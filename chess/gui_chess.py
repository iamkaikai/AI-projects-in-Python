# brew install pyqt
from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QWidget
import sys
import chess, chess.svg
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from ChessGame import ChessGame
from Alpha_Beta_Pruning import A_B_Pruning
from Alpha_Beta_Pruning_basic import A_B_Pruning_basic
from iterative_minimaxAI import MinimaxAI_iterative
from HumanPlayer import HumanPlayer

import random
from time import sleep


class ChessGui:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.game = ChessGame(player1, player2)
        self.app = QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50, 50, 500, 500)
        self.svgWidget.show()


    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_move)
        self.timer.start(10)

        self.display_board()

    def display_board(self):
        svgboard = chess.svg.board(self.game.board)

        svgbytes = QByteArray()
        svgbytes.append(svgboard)
        self.svgWidget.load(svgbytes)


    def make_move(self):
        if self.game.is_game_over():
            print('Game Over!')
            result = self.game.board.result()
            if result == "1-0":
                print("⬜ White wins!")
            elif result == "0-1":
                print("⬛ Black wins!")
            elif result == "1/2-1/2":
                print("🟨 It's a draw!")
            self.timer.stop()  # Stop the QTimer
            print(self.game.board)
            sleep(10)
            sys.exit(gui.app.exec_())
            return 
        print("making move, white turn " + str(self.game.board.turn))
        self.game.make_move()
        self.display_board()


if __name__ == "__main__":

    # random.seed(1)

    # player_ronda = RandomAI()
    # to do: gui does not work well with HumanPlayer, due to input() use on stdin conflict
    # with event loop.
    
    # go first
    # player1 = RandomAI()
    # player1 = MinimaxAI(2)
    player1 = A_B_Pruning(3)
    # player1 = A_B_Pruning_basic(2)
    
    # go second
    # player2 = RandomAI()
    # player2 = MinimaxAI(1)
    # player2 = A_B_Pruning(20)
    player2 = A_B_Pruning_basic(2)
    
    
    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)
    gui.start()
    sys.exit(gui.app.exec_())
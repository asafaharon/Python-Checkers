import pygame
from checkers.constants import RED, GREEN, BLUE, SQUARE_SIZE
from checkers.board import Board
from checkers.board import Board


# department responsible for checking the legality of a move and also for marking legal moves
# and also for switching between the players' turns

class Game:
    def __init__(self, win):
        self.selected = None
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    # A boolean function that returns true or false to
    # whether the current player is allowed to make the move he is about to make
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    # function that colors each legal square center for a move in blue in order to show the player
    # which move is a legal move
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    # A function that replaces after each move who is allowed to play in the next move
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = GREEN
        else:
            self.turn = RED

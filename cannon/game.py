from doctest import ELLIPSIS_MARKER
import pygame

from cannon.board import Board
from cannon.piece import Piece, Town
from cannon.const import LIGHT, DARK, BLUE, ROWS, COLS

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = DARK
        self.valid_moves = {}
        self.chickendinner = None
    
    def reset(self):
        self._init()

    def update(self):
        self.board.draw(self.win)
        self.board.draw_valid_moves(self.win, self.valid_moves)
        pygame.display.update()
    
    def winner(self):
        if self.chickendinner:
            if self.chickendinner == DARK:
                return "DARK: YOUR WINNER!"
            else:
                return "LIGHT: YOUR WINNER!"
        return None
    
    def select_town_place(self, row, col, color):
        valid_towns = [(0,n+1) for n in range(COLS-2)] if color == DARK else [(ROWS-1,n+1) for n in range(COLS-2)]
        if (row, col) in valid_towns:
            self.board[row][col] = Town(row, col, color)
            self.change_turn()
        else:
            return False
    
    def select(self, row, col):
        if self.selected:
            result = self._move(self.selected, row, col)
            if not result:
                self.valid_moves = {}
                self.selected = None
                self.select(row, col)
        # deleted else
        piece = self.board.get_piece(row, col)
        if type(piece) == Piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            print(f"{piece.color} selected {piece.row}, {piece.col}")
            return True
        
        return False

    def _move(self, piece, row, col):
        move = self.valid_moves.get((row, col))
        if move:
            if move[0] == "move":
                self.board.move(piece, row, col)
            elif move[0] == "take":
                self.board.move(piece, row, col)
                if type(piece) == Piece:
                    self.capture_piece(piece.color)
                else:
                    self.winner = piece.color

            elif move[0] == "shoot":
                self.board.remove(row, col)
                if type(piece) == Piece:
                    self.capture_piece(piece.color)
                else:
                    self.winner = piece.color
                print(self.board.light_pieces, self.board.dark_pieces)
            else:
                raise Exception("Invalid move type")
            self.change_turn()
        else:
            return False
        return True
    
    def capture_piece(self, color):
        if color == DARK:
            self.board.light_pieces -= 1
        else:
            self.board.dark_pieces -= 1

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == LIGHT:
            self.turn = DARK
        else:
            self.turn = LIGHT

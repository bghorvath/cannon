import pygame

from cannon.board import Board
from cannon.piece import Piece, Town
from cannon.const import LIGHT, DARK, ROWS, COLS

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = DARK
        self.valid_moves = []
        self.valid_towns = {DARK: [(0,n+1) for n in range(COLS)-2], LIGHT: [(ROWS-1,n+1) for n in range(COLS)-2]}
    
    def reset(self):
        self._init()

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()
    
    def select_town_place(self, row, col, color):
        if color == self.turn and (row, col) in self.valid_town_row[color]:
            town = Town(row, col, color)
            self.board[row][col] = town
            self.change_turn()
        else:
            return False
    
    def select(self, row, col):
        if self.selected:
            result = self.move(self.selected, row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        else:
            piece = self.board.get_piece(row, col)
            if type(piece) == Piece and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                print(f"{piece.color} selected {piece.row}, {piece.col}")
                return True
        
        return False
        

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
        else:
            return False
        
        return True
    
    def change_turn(self):
        if self.turn == LIGHT:
            self.turn == DARK
        else:
            self.turn == LIGHT

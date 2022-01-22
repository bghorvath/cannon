# standard imports
from random import choice

# third party imports
import pygame

# local imports
from cannon.board import Board
from cannon.piece import Piece
from cannon.const import LIGHT, DARK

class Game:
    """
    Wrapper for a single cannon game for a single window.

    Parameters:
        win (pygame.Surface): The window to draw the game on.
    """
    def __init__(self, win):
        """
        Initialize the game on the window. Calls _init method which is separate so it can be reset without reloading window.

        Parameters:
            win (pygame.Surface): The window to draw the game on.
        """
        self._init()
        self.win = win
    
    def _init(self):
        """
        Load/reload the game.

        Parameters:
            selected (Piece): The selected piece.
            board (Board): The board to draw and play on, all gameplay related method is stored inside.
            turn (tuple): The color of the player whose turn it is.
            valid_moves (dict): Dictionary of valid moves for the selected piece.
            towns (set): Set of towns on the board, needed for first move (placing the 2 towns).
        """
        self.selected = None
        self.board = Board()
        self.turn = DARK
        self.valid_moves = {}
    
    def reset(self):
        """
        Reset the game without changing the window.
        """
        self._init()

    def update(self):
        """
        Update the window with the current game state.
        """
        self.board.draw(self.win)
        self.board.draw_valid_moves(self.win, self.valid_moves)
        pygame.display.update()
    
    def chickendinner(self):
        """
        Return a winner if the game is over.

        Returns:
            str: The winner if the game is over, else None.
        """
        if self.board.towns.get(LIGHT) == 0:
            return "DARK"
        if self.board.towns.get(DARK) == 0:
            return "LIGHT"
        return None
    
    def select(self, row, col):
        """
        Try to select a piece on the board, if selected, move the piece. Recursive, only select if valid, else try again. If first round, place town.
        
        Parameters:
            row (int): Selected row.
            col (int): Selected column.
        
        Returns:
            bool: True if selection was successful, False if not.
        """
        if len(self.board.towns) < 2:
            result = self.board.place_town(row, col, self.turn)
            if result:
                self.change_turn()
        else:
            if self.selected:
                result = self._move(self.selected, row, col)
                if not result:
                    self.valid_moves = {}
                    self.selected = None
                    self.select(row, col)
            piece = self.board.get_piece(row, col)
            if type(piece) == Piece and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                # print(f"{piece.color} selected {piece.row}, {piece.col}")
                return True
        
        return False

    def _move(self, piece, row, col):
        """
        Make the desired move. If simple move, move the piece. If capture, move the piece and remove the captured piece.
            If shoot, remove the piece. If removed piece is Town, end the game.
        
        Parameters:
            piece (Piece): The piece to move.
            row (int): The row to move to.
            col (int): The column to move to.
        
        Returns:
            bool: True if move was successful, False if not.
        """
        move = self.valid_moves.get((row, col))
        if move:
            move_type = move[0]
            if move_type == "move":
                self.board.move(piece, row, col)
            elif move_type in {"capture", "shoot"}:
                enemy_piece = move[1]
                enemy_color = enemy_piece.color
                if move_type == "capture":
                    self.board.move(piece, row, col)
                else:
                    self.board.remove(row, col)
                if type(enemy_piece) == Piece:
                    self.board.deduct_piece(enemy_color)
                else:
                    self.board.towns[enemy_color] = 0
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        """
        Change the turn to the other player and clear the valid moves.
        """
        self.valid_moves = {}
        if self.turn == LIGHT:
            self.turn = DARK
        else:
            self.turn = LIGHT

    def random_town(self):
        color_valid_towns = self.board.valid_towns.get(self.turn)
        row, col = choice(color_valid_towns)
        self.board.place_town(row, col, self.turn)
        
        self.change_turn()

    def ai_move(self, board):
        self.board = board
        self.change_turn()

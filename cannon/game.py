# third party imports
import pygame

# local imports
from cannon.board import Board
from cannon.piece import Piece, Town
from cannon.const import LIGHT, DARK, ROWS, COLS

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
            chickendinner (tuple): The color of the player who won the game. If not None, the game is over. Resets with restart.
        """
        self.selected = None
        self.board = Board()
        self.turn = DARK
        self.valid_moves = {}
        self.towns = set()
        self.chickendinner = None
    
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
    
    def winner(self):
        """
        Return a winner if the game is over.

        Returns:
            str: The winner if the game is over, else None.
        """
        if self.chickendinner:
            if self.chickendinner == DARK:
                return "DARK"
            else:
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
        if len(self.towns) < 2:
            valid_towns = [(0,n+1) for n in range(COLS-2)] if self.turn == LIGHT else [(ROWS-1,n+1) for n in range(COLS-2)]
            if (row, col) in valid_towns:
                town = Town(row, col, self.turn)
                self.towns.add(town)
                self.board.board[row][col] = town
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
            if move[0] == "move":
                self.board.move(piece, row, col)
            elif move[0] == "capture":
                self.board.move(piece, row, col)
                if type(move[1]) == Piece:
                    self.deduct_piece(piece.color)
                    # print(self.board.light_pieces, self.board.dark_pieces)
                else:
                    self.chickendinner = piece.color
            elif move[0] == "shoot":
                self.board.remove(row, col)
                if type(move[1]) == Piece:
                    self.deduct_piece(piece.color)
                    # print(self.board.light_pieces, self.board.dark_pieces)
                else:
                    self.chickendinner = piece.color
            self.change_turn()
        else:
            return False
        return True
    
    def deduct_piece(self, color):
        """
        If a piece is captured or shot, deduct it from the player's piece count.
        """
        if color == DARK:
            self.board.light_pieces -= 1
        else:
            self.board.dark_pieces -= 1

    def change_turn(self):
        """
        Change the turn to the other player and clear the valid moves.
        """
        self.valid_moves = {}
        if self.turn == LIGHT:
            self.turn = DARK
        else:
            self.turn = LIGHT

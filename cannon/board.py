import pygame
from cannon.piece import Piece, Town
from cannon.const import WIDTH, HEIGHT, BORDER, ROWS, COLS, GRID, LIGHT, DARK, PADDING, PIECE_RADIUS, OUTLINE, LIGHT_BROWN, BROWN, BLACK, WHITE, BLUE

class Board:
    def __init__(self):
        self.board = []# [[0 for x in range(constants.ROWS)] for y in range(10)]
        self.light_piece = self.dark_piece = 15

        self.create_board()
    
    def draw_grid(self, win):
        win.fill(BROWN)
        pygame.draw.rect(win, LIGHT_BROWN, (BORDER, BORDER, WIDTH-BORDER*2, HEIGHT-BORDER*2))
        for row in range(ROWS-1):
            pygame.draw.line(win, BLACK, (BORDER+row*GRID, BORDER), (BORDER+row*GRID, HEIGHT-BORDER))
        for col in range(COLS-1):
            pygame.draw.line(win, BLACK, (BORDER, BORDER+col*GRID), (WIDTH-BORDER, BORDER+col*GRID))
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == 0:
                    if row in {1,2,3}:
                        self.board[row].append(Piece(row, col, LIGHT))
                    else:
                        self.board[row].append(0)
                elif col % 2 == 1:
                    if row in {6,7,8}:
                        self.board[row].append(Piece(row, col, DARK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0) # NOTE don't forget to add Town as soon as players choose

    def draw(self, win):
        self.draw_grid(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_piece(self, row, col):
        try:
            piece = self.board[row][col]
            if type(piece) == Piece:
                return piece
            else:
                return 0
        except IndexError:
            return 0

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        # remove only the current piece's possible moves after moving from the moves dict
        # and if piece disappeared, the pieces its in 1 cannon with
        # NOTE: if 3 pieces are in the same row, then cannon function

    def check_piece_color(self, row, col, color):
        piece = self.board[row][col]
        if type(piece) == Piece and piece.color == color:
            return True
        else:
            return False
    
    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row
        col = piece.col
        moves.update(check_leftcannon(piece))
    
        def check_leftcannon(self, piece):
            if self.check_piece_color(piece.row, piece.col, piece.color):
                return (piece.row, piece.col-2)
        
        def check_rightcannon(self, piece):
            if self.check_piece_color(piece.row, piece.col, piece.color):
                return (piece.row, piece.col+2)
        
        
        
    if check_leftcannon(self, row, col):
        moves[(row, left)] = True


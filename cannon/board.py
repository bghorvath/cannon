from random import shuffle
import pygame
from cannon.piece import Piece, Town
from cannon.params import WIDTH, HEIGHT, BORDER, ROWS, COLS, GRID, LIGHT, DARK, PIECE_RADIUS, LIGHT_BROWN, BROWN, BLACK, WHITE, BLUE

class Board:
    def __init__(self):
        self.board = {}
        self.light_pieces = self.dark_pieces = 15
        self.valid_towns = {LIGHT: [(0,n+1) for n in range(COLS-2)], DARK: [(ROWS-1,n+1) for n in range(COLS-2)]}
        self.towns = {}
        self.no_move = None

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
            self.board[row] = {}
            for col in range(COLS):
                if col % 2 == 0:
                    if row in {1,2,3}:
                        self.board[row][col] = Piece(row, col, LIGHT)
                    else:
                        self.board[row][col] = 0
                elif col % 2 == 1:
                    if row in {6,7,8}:
                        self.board[row][col] = Piece(row, col, DARK)
                    else:
                        self.board[row][col] = 0

    def draw(self, win):
        self.draw_grid(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def place_town(self, row, col, turn):
        color_valid_towns = self.valid_towns.get(turn)
        if (row, col) in color_valid_towns:
            town = Town(row, col, turn)
            self.towns[turn] = town
            self.board[row][col] = town
        else:
            return False
        return True
        
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
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], 0
        piece.move(row, col) # NOTE: watch out, this doesn't call the move to the taken piece, but this shouldn't be a problem
        # remove only the current piece's possible moves after moving from the moves dict
        # and if piece disappeared, the pieces its in 1 cannon with

    def remove(self, row, col):
        self.board[row][col] = 0

    def deduct_piece(self, color):
        """
        If a piece is captured or shot, deduct it from the player's piece count.
        """
        if color == DARK:
            self.dark_pieces -= 1
        else:
            self.light_pieces -= 1

    def parse_board(self, row, col, color):
        step = {LIGHT: 1, DARK: -1}.get(color)
        proximity = {}
        for field in [{"left"}, {"right"}, {"up"}, {"down"}, {"left","up"}, {"left","down"}, {"right","up"}, {"right","down"}]:
            for count in [1, 2, 3, 4, 5]:
                newrow = row
                newcol = col
                field_name = ""
                if "left" in field:
                    newcol = col + step * count
                    field_name += "left"
                if "right" in field:
                    newcol = col - step * count
                    field_name += "right"
                if "up" in field:
                    newrow = row + step * count
                    field_name += "up"
                if "down" in field:
                    newrow = row - step * count
                    field_name += "down"
                field_name = field_name+str(count) # creating field names, e.g. leftup3, down5, etc.

                proximity[field_name] = {"piece": self.board.get(newrow,{}).get(newcol), "pos": (newrow, newcol)} # assigning field value (piece / 0 / None) and position

        field_type_dict = {}
        for k,v in proximity.items():
            piece = v["piece"]
            pos = v["pos"]
            if type(piece) in {Piece, Town}:
                if piece.color != color:
                    field_type_dict[k] = {"field_type": "enemy", "piece_type": type(piece), "pos": pos, "piece": piece}
                else:
                    field_type_dict[k] = {"field_type": "friendly", "piece_type": type(piece), "pos": pos, "piece": piece}
            elif piece == 0:
                field_type_dict[k] = {"field_type": "empty", "piece_type": type(piece), "pos": pos, "piece": piece}
            else:
                field_type_dict[k] = {"field_type": "wall", "piece_type": None, "pos": None, "piece": None}
        
        return field_type_dict
    
    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row
        col = piece.col
        color = piece.color

        # could make it better by only calculating this once, using "dark"/"light" instead of enemy/friedly
        # calculate once for whole board ?
        
        prox = self.parse_board(row, col, color)

        # basic moves
        for move in ["leftup1", "up1", "rightup1"]:
            pos = prox[move]["pos"]
            piece = prox[move]["piece"]
            if prox[move]["field_type"] == "empty":
                moves[pos] = ("move", None)
            elif prox[move]["field_type"] == "enemy":
                moves[pos] = ("capture", piece)
        
        # retreat
        if any(v["field_type"] == "enemy" and v["piece_type"] == Piece for v in [prox["up1"], prox["left1"], prox["right1"], prox["leftup1"], prox["rightup1"]]):
            for move in ["down", "leftdown", "rightdown"]:
                if prox[move+"1"]["field_type"] == "empty" and prox[move+"2"]["field_type"] == "empty":
                    pos = prox[move+"2"]["pos"]
                    moves[pos] = ("move", None)

        # left-right takes
        for move in ["left1", "right1"]:
            pos = prox[move]["pos"]
            piece = prox[move]["piece"]
            if prox[move]["field_type"] == "enemy":
                moves[pos] = ("capture", piece)
        
        # cannon moves and shoots
        for move in ["up", "down", "left", "right", "leftup", "leftdown", "rightup", "rightdown"]:
            if prox[move+"1"]["field_type"] == "friendly" and prox[move+"1"]["piece_type"] == Piece and prox[move+"2"]["field_type"] == "friendly" and prox[move+"2"]["piece_type"] == Piece and prox[move+"3"]["field_type"] == "empty":
                pos = prox[move+"3"]["pos"]
                moves[pos] = ("move", None)
                if prox[move+"4"]["field_type"] == "enemy":
                    pos = prox[move+"4"]["pos"]
                    piece = prox[move+"4"]["piece"]
                    moves[pos] = ("shoot", piece)
                if prox[move+"4"]["field_type"] == "empty" and prox[move+"5"]["field_type"] == "enemy":
                    pos = prox[move+"5"]["pos"]
                    piece = prox[move+"5"]["piece"]
                    moves[pos] = ("shoot", piece)
        
        return moves

    def draw_valid_moves(self, win, moves):
        for move, move_type in moves.items():
            if move_type[0] == "move":
                move_color = WHITE
            else:
                move_color = BLUE
            row, col = move
            pygame.draw.circle(win, move_color, (BORDER + col * GRID, BORDER + row * GRID), PIECE_RADIUS*0.5)

    def get_valid_pieces(self, color):
        valid_pieces = [v_v for _,v in self.board.items() for _, v_v in v.items() if type(v_v) == Piece and v_v.color == color]
        shuffle(valid_pieces)
        return valid_pieces

    def distance_from_opposite_town(self, piece):
        if piece.color == DARK:
            town = self.towns.get(LIGHT)
        else:
            town = self.towns.get(DARK)

        return abs(piece.row-town.row)+abs(piece.col-town.col)

    def evaluate(self, color):
        # num_pieces = 0
        # min_town_distance = float("-inf")
        # if 
        # for piece in self.get_valid_pieces(color):
        #     num_pieces += 1
        #     town_distance = self.distance_from_opposite_town(piece)
        #     if town_distance < min_town_distance:
        #         min_town_distance = town_distance
        if color == LIGHT:
            return self.light_pieces - self.dark_pieces + 100 * (bool(self.towns.get(LIGHT)) - bool(self.towns.get(DARK)))
        else:
            return -1 * (self.light_pieces - self.dark_pieces + 100 * (bool(self.towns.get(LIGHT)) - bool(self.towns.get(DARK))))
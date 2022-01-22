from copy import deepcopy

import pygame

from cannon.const import DARK, LIGHT
from cannon.piece import Piece

# as first move, the AI should select the town randomly

class Ai:
    def __init__(self, ai_color):
        self.minimax_param_dict = self.get_minimax_params()
        self.ai_color = ai_color

    @staticmethod
    def get_minimax_params():
        return {
            True: {"score_boundary": float("-inf"), "color": LIGHT, "extrema": max},
            False: {"score_boundary": float("inf"), "color": DARK, "extrema": min}
        }
    
    def call_minimax(self, board, depth):
        if self.ai_color == DARK:
            return self.minimax(board, depth, False)
        else:
            return self.minimax(board, depth, True)
    
    def minimax(self, board, depth, max_player):
        if depth == 0 or board.towns.get(DARK) == 0 or board.towns.get(LIGHT) == 0:
            return board.evaluate(), board
        
        minimax_params = self.minimax_param_dict[max_player]

        best_score = minimax_params["score_boundary"]
        best_move_board = None
        for move_board in self.get_all_move_boards(board, minimax_params["color"]):
            score = self.minimax(move_board, depth-1, not max_player)[0]
            best_score = minimax_params["extrema"](best_score, score)
            if best_score == score:
                best_move_board = move_board
        
        return best_score, best_move_board
    
    # def minimax(self, board, depth, max_player):
    #     if depth == 0 or board.towns.get(LIGHT) == 0 or board.towns.get(LIGHT) == 0:
    #         return board.evaluate(), board
        
    #     if max_player:
    #         max_score = float("-inf")
    #         best_move_board = None
    #         for move_board in self.get_all_move_boards(board, LIGHT):
    #             score = self.minimax(move_board, depth-1, False)[0]
    #             max_score = max(max_score, score)
    #             if max_score == score:
    #                 best_move_board = move_board
                
    #         return max_score, best_move_board
    #     else:
    #         min_score = float("inf")
    #         best_move_board = None
    #         for move_board in self.get_all_move_boards(board, DARK):
    #             score = self.minimax(move_board, depth-1, True)[0]
    #             min_score = min(min_score, score)
    #             if min_score == score:
    #                 best_move_board = move_board
            
    #         return min_score, best_move_board

    def get_all_move_boards(self, board, color):
        move_boards = []
        for piece in board.get_valid_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for pos, move in valid_moves.items():
                row, col = pos
                move_type, enemy_piece = move
                board_ = deepcopy(board)
                piece_ = board_.get_piece(piece.row, piece.col)
                self.simulate_move(board_, piece_, row, col, move_type, enemy_piece)
                move_boards.append(board_)
        
        return move_boards
    
    @staticmethod
    def simulate_move(board, piece, row, col, move_type, enemy_piece):
        if move_type == "move":
            board.move(piece, row, col)
        elif move_type in {"capture", "shoot"}:
            enemy_color = enemy_piece.color
            if move_type == "capture":
                board.move(piece, row, col)
            else:
                board.remove(row, col)
            if type(enemy_piece) == Piece:
                board.deduct_piece(enemy_color)
            else:
                board.towns[enemy_color] = 0


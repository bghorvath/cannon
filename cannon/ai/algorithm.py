from copy import deepcopy

from cannon.params import DARK, LIGHT
from cannon.piece import Piece

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
    
    def call_algorithm(self, board, depth):
        if self.ai_color == DARK:
            # return self.minimax(board, depth, False)
            # return self.negamax(board, depth, -1)
            pass
            # return self.alpha_beta_negamax(board, depth, float("inf"), float("-inf"), -1)
        else:
            # return self.minimax(board, depth, True)
            # return self.negamax(board, depth, 1)
            return self.alpha_beta_negamax(board, depth, float("-inf"), float("inf"), 1)
    
    def minimax(self, board, depth, max_player):
        if depth == 0 or board.towns.get(DARK) == 0 or board.towns.get(LIGHT) == 0:
            return board.evaluate(), board
        
        minimax_params = self.minimax_param_dict[max_player]

        best_score = minimax_params["score_boundary"]
        best_move_board = None
        for move_board in self.get_all_move_boards(board, minimax_params["color"]):
            if depth == 1:
                print(depth)
            score = self.minimax(move_board, depth-1, not max_player)[0]
            best_score = minimax_params["extrema"](best_score, score)
            if best_score == score:
                best_move_board = move_board
        
        return best_score, best_move_board
    
    def negamax(self, board, depth, max_player):
        color = LIGHT if max_player == 1 else DARK
        if depth == 0 or board.towns.get(DARK) == 0 or board.towns.get(LIGHT) == 0: # or board.no_move:
            return board.evaluate(color), board

        best_score = float("-inf")
        best_move_board = None
        for move_board, pos, move, piece_pos in self.get_all_move_boards(board, color):
            score = -self.negamax(move_board, depth-1, -max_player)[0]
            if score > best_score:# best_score = max(best_score, score)
                best_score = score
                best_move_board = move_board
        
        return best_score, best_move_board

    def alpha_beta_negamax(self, board, depth, alpha, beta, max_player):
        color = LIGHT if max_player == 1 else DARK
        if depth == 0 or board.towns.get(DARK) == 0 or board.towns.get(LIGHT) == 0: # or board.no_move:
            return board.evaluate(color), board

        # move ordering
        best_score = float("-inf")
        best_move_board = None
        best_pos = None
        best_move = None
        for move_board, pos, move, piece_pos in self.get_all_move_boards(board, color):
            score = -1*self.alpha_beta_negamax(move_board, depth-1, -beta, -alpha, -max_player)[0]
            if score > best_score:
                best_score = score
                best_move_board = move_board
                best_pos = pos
                best_piece_pos = piece_pos
                best_move = move
            if best_score > alpha:
                alpha = best_score
            if alpha >= beta:
                break
        
        return best_score, best_move_board

    def iterative_deepening(self):
        pass

    def get_all_move_boards(self, board, color):
        move_boards = []
        for piece in board.get_valid_pieces(color):
            piece_row, piece_col = piece.row, piece.col
            valid_moves = board.get_valid_moves(piece)
            for pos, move in valid_moves.items():
                row, col = pos
                move_type, enemy_piece = move
                board_ = deepcopy(board)
                piece_ = board_.get_piece(piece_row, piece_col)
                board_ = self.simulate_move(board_, piece_, row, col, move_type, enemy_piece)
                move_boards.append([board_, pos, move, (piece_row, piece_col)]) # board_)#
        if len(move_boards) > 0:
            return move_boards
        board.no_move = color
        return [board]
    
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
        return board


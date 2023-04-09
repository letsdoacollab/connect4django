import random
import math
import time


global start_time
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4
EMPTY_SLOT = 0
PLAYER_PIECE = 1
AI_PIECE = 2


def is_valid_location(board, ai_move_col):
    return board[ROW_COUNT-1][ai_move_col] == 0


def get_next_open_row(board, ai_move_col):
    for i in range(ROW_COUNT):
        if board[i][ai_move_col] == 0:
            return i


def drop_peace(board, open_row, column, piece):
    board[open_row][column] = piece


def wining(game_board, player_piece):
    # Check Horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if (game_board[r][c] == player_piece and game_board[r][c+1] == player_piece
                    and game_board[r][c+2] == player_piece and game_board[r][c+3] == player_piece):
                return True

    # Check Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if (game_board[r][c] == player_piece and game_board[r+1][c] == player_piece
                    and game_board[r+2][c] == player_piece and game_board[r+3][c] == player_piece):
                return True

    # Check Positive diagonal Slope
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if (game_board[r][c] == player_piece and game_board[r+1][c+1] == player_piece
                    and game_board[r+2][c+2] == player_piece and game_board[r+3][c+3] == player_piece):
                return True

    # Check Negative diagonal slope
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if (game_board[r][c] == player_piece and game_board[r-1][c+1] == player_piece
                    and game_board[r-2][c+2] == player_piece and game_board[r-3][c+3] == player_piece):
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_SLOT) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY_SLOT) == 1:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY_SLOT) == 1:
        score -= 4
    return score


def score_position(board, piece):
    score = 0
    # score Center column
    center_array = [int(_) for _ in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count

    # score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(_) for _ in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(_) for _ in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # score Positive Diagonal slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # score Negative Diagonal Slope
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[(r+3)-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def terminal_node(board):
    return wining(board, PLAYER_PIECE) or wining(board, AI_PIECE) or len(get_valid_locations_to_drop(board)) == 0


def minimax_iterative_deepening(board, depth, alpha, beta, maximizing_player):
    best_move = 0
    move_time = 5
    for current_depth in range(1, depth+1):
        column, value = minimax_alpha_beta_depth_limit(board, current_depth, alpha, beta, maximizing_player)
        if time.time() - start_time >= move_time:
            break
        best_move = column
    return best_move


def minimax_alpha_beta_depth_limit(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations_to_drop(board)
    is_terminal_node = terminal_node(board)
    move_time = 5
    if depth == 0 or is_terminal_node or (time.time() - start_time >= move_time):
        if is_terminal_node:
            if wining(board, AI_PIECE):
                return None, math.inf
            elif wining(board, PLAYER_PIECE):
                return None, -math.inf
            else:
                return None, 0
        elif depth == 0:
            return None, score_position(board, AI_PIECE)
        else:
            return None, score_position(board, AI_PIECE)

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for c in valid_locations:
            row = get_next_open_row(board, c)
            temp_board = board.copy()
            drop_peace(temp_board, row, c, AI_PIECE)
            new_score = minimax_alpha_beta_depth_limit(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = c
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing Player
        value = math.inf
        column = random.choice(valid_locations)
        for c in valid_locations:
            row = get_next_open_row(board, c)
            temp_board = board.copy()
            drop_peace(temp_board, row, c, PLAYER_PIECE)
            new_score = minimax_alpha_beta_depth_limit(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = c
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations_to_drop(board):
    valid_locations = []
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            valid_locations.append(c)
    return valid_locations


def ai_move(board):
    global start_time
    start_time = time.time()
    move_column = minimax_iterative_deepening(board, 5, -math.inf, math.inf, True)
    return move_column

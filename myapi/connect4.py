import numpy as np
from myapi.connect4ai import ai_move

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 1
AI = 2
PLAYER_PIECE = 1
AI_PIECE = 2


def create_board():
    board_layout = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board_layout


def drop_peace(game_board, open_row, column, player_piece):
    game_board[open_row][column] = player_piece


def is_valid_location(game_board, player_move_col):
    return game_board[ROW_COUNT-1][player_move_col] == 0


def get_next_open_row(game_board, player_move_col):
    for i in range(ROW_COUNT):
        if game_board[i][player_move_col] == 0:
            return i


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


def connect4game(player_column):
    board = create_board()
    game_over = False
    winner = 0
    move_col = player_column
    if is_valid_location(board, move_col):
        row = get_next_open_row(board, move_col)
        drop_peace(board, row, move_col, PLAYER_PIECE)
        if wining(board, PLAYER_PIECE):
            game_over = True
            winner = 2

    move_col = ai_move(board)
    if is_valid_location(board, move_col):
        row = get_next_open_row(board, move_col)
        drop_peace(board, row, move_col, AI_PIECE)
        if wining(board, AI_PIECE):
            game_over = True
            winner = 1
    if game_over:
        return move_col, winner
    else:
        return move_col

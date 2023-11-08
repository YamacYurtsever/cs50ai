"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    move_count = 0
    for row in board:
        for square in row:
            if square != EMPTY:
                move_count += 1
    if move_count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    resulting_board = copy.deepcopy(board)
    if resulting_board[action[0]][action[1]] == EMPTY:
        resulting_board[action[0]][action[1]] = player(board)
        return resulting_board
    else:
        raise ValueError("Invalid action")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    players = [X, O]

    for player in players:
        # Check horizontal triples
        for row in board:
            if all(square == player for square in row):
                return player

        # Check vertical triples
        for i in range(len(board[0])):
            if all(row[i] == player for row in board):
                return player

        # Check diagonal triples
        if all(board[i][i] == player for i in range(len(board))):
            return player
        if all(board[i][(len(board) - 1) - i] == player for i in range(len(board))):
            return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or all(square is not EMPTY for row in board for square in row):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        best_value = -float("inf")
        best_action = None
        for action in actions(board):
            value = min_value(result(board, action), -
                              float("inf"), float("inf"))
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    else:
        best_value = float("inf")
        best_action = None
        for action in actions(board):
            value = max_value(result(board, action), -
                              float("inf"), float("inf"))
            if value < best_value:
                best_value = value
                best_action = action
        return best_action


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    value = -float("inf")
    for action in actions(board):
        value = max(value, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, value)
        if value >= beta:
            break
    return value


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    value = float("inf")
    for action in actions(board):
        value = min(value, max_value(result(board, action), alpha, beta))
        beta = min(beta, value)
        if value <= alpha:
            break
    return value

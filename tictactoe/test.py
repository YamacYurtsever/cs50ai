import tictactoe

X = "X"
O = "O"
E = None

board = [[X, O, X],
         [O, E, E],
         [E, E, E]]


def main():
    # print(tictactoe.player(board))
    # print(tictactoe.actions(board))
    # print(tictactoe.result(board, list(tictactoe.actions(board))[0]))
    # print(tictactoe.winner(board))
    # print(tictactoe.terminal(board))
    # print(tictactoe.utility(board))
    print(tictactoe.minimax(board))


main()

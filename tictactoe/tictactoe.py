"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
decider = X
Opp = {
    "X": "O",
    "O": "X"
}

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
    # print("decider" ,decider)
    # print("moves",moves_made(board))
    return X if (board[0].count(EMPTY) + board[1].count(EMPTY) + board[2].count(EMPTY)) % 2 == 0 else O

    # return X if (board[0].count(X) + board[1].count(X) + board[2].count(X)) > (
    #             board[0].count(O) + board[1].count(O) + board[2].count(O)) else O

    # x = board.count(X)
    # o = board.count(O)
    # return X if x>o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # global decider
    # decider = 1
    action_list = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action_list.append((i, j))
    return action_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = copy.deepcopy(board)
    id = player(board)
    i, j = action
    if new_board[i][j] != EMPTY:
        print(action)
        print(new_board)
        raise NotImplementedError

    new_board[i][j] = id
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    id = Opp[player(board)]

    for i in range(0, 3):
        if board[0][i] == board[1][i] == board[2][i] == id:
            return id
        elif board[i][0] == board[i][1] == board[i][2] == id:
            return id
    if board[0][0] == board[1][1] == board[2][2] == id:
        return id
    elif board[2][0] == board[1][1] == board[0][2] == id:
        return id
    else:
        return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != EMPTY:
        return True
    elif board[0].count(EMPTY) == 0 and board[1].count(EMPTY) == 0 and board[2].count(EMPTY) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    util = {X: 1, O: -1}

    if decider == O:
        util = {X: -1, O: 1}
    win = winner(board)
    if win == X:
        return util[X]
    elif win == O:
        return util[O]
    else:
        return 0


def minimax(board):
    if terminal(board):
        return None
    else:
        act = (9, 9)
        # default value act passed since function has a parametric requirement
        val, act = max_value(board, act)
        return act


def max_value(board, act):
    if terminal(board):
        return utility(board), act
    else:
        max_val = -2
        f_action = act
        arr = []
        for action in actions(board):
            val, _ = min_value(result(board, action), action)
            if val > max_val:
                max_val = val
                arr.append(max_val)
                # if arr == [-1, 1] and action != f_action:
                #     print(action)
                f_action = action
                if max_val == 1:
                    break
        return max_val, f_action


def min_value(board, act):
    if terminal(board):
        return utility(board), act
    else:
        min_val = 2
        f_action = act
        for action in actions(board):
            val, _ = max_value(result(board, action), action)
            if val < min_val:
                min_val = val
                # print(min_val)
                f_action = action
                if min_val == -1:
                    break
        return min_val, f_action


def moves_made(board):
    return 9 - (board[0].count(EMPTY) + board[1].count(EMPTY) + board[2].count(EMPTY))

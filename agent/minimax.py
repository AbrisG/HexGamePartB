from referee.game import PlayerColor, SpawnAction, BOARD_N, HexPos, SpreadAction, HexDir, Action
from referee.game.board import Board as OurBoard


def evaluate_board(board) -> int:
    """
    Evaluate the board and return a score.
    """
    maximizing_player = PlayerColor.RED

    def power_parity(board):
        return board._color_power(maximizing_player) - board._color_power(maximizing_player.opponent)

    # TODO:
    #  (1) Brainstorm some other evaluation functions
    #  (2) Order the actions based on *likely* utility to achieve better results with alpha-beta pruning
    #  (3) Implement memoization for performance tuning?

    return power_parity(board)


def generate_valid_spawn_actions(board) -> list[Action]:
    """
    Generate a list of valid spawn actions. Defined as all cells not currently occupied.
    """
    if board._total_power >= BOARD_N * 2:
        return []
    all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
    available_cells = [cell for cell in all_cells if not board._cell_occupied(cell)]
    return [SpawnAction(cell) for cell in available_cells]


def generate_valid_spread_actions(board, maximizing_player) -> list[Action]:
    """
    Generate a list of valid spread actions. Defined all 6 directions for every cell owned by the player.
    """
    color = PlayerColor.RED if maximizing_player else PlayerColor.BLUE
    all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
    colored_cells = [cell for cell in all_cells if board[cell].player == color]
    return [SpreadAction(cell, direction) for cell in colored_cells for direction in HexDir]


def generate_valid_child_boards(parent_board, maximizing_player) -> list[OurBoard]:
    """
    Generate a list of valid child boards.
    """
    actions = generate_valid_spawn_actions(parent_board) + \
              generate_valid_spread_actions(parent_board, maximizing_player)

    child_boards = []
    for action in actions:
        new_board = parent_board.copy()
        new_board.apply_action(action)
        child_boards.append(new_board)

    return child_boards


def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning.
    """
    if depth == 0 or board.game_over:
        return evaluate_board(board), board, depth

    if maximizing_player:
        value = -100000000000
        for child_board in generate_valid_child_boards(board, maximizing_player):
            new_value, new_board, new_depth = minimax(child_board, depth - 1, alpha, beta, False)
            if new_value > value:
                value = new_value
                best_board = new_board
                best_depth = new_depth
            if value > beta:
                break
            alpha = max(value, alpha)
        return value, best_board, best_depth
    else:
        value = 100000000000
        for child_board in generate_valid_child_boards(board, maximizing_player):
            new_value, new_board, new_depth = minimax(child_board, depth - 1, alpha, beta, True)
            if new_value < value:
                value = new_value
                best_board = new_board
                best_depth = new_depth
            if value < alpha:
                break
            beta = min(value, beta)
        return value, best_board, best_depth



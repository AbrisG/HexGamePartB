import time

from referee.game import PlayerColor, SpawnAction, BOARD_N, HexPos, SpreadAction, HexDir, Action
from agent.ourboard import OurBoard
from referee.game.board import CellState


def evaluate_board(board, a1, a2):
    """
    Evaluate the board and return a score. Metrics based on power and cell parity.
    Cell parity receives higher weighting.
    """
    def power_parity(board):
        return board._color_power(PlayerColor.RED) - board._color_power(PlayerColor.BLUE)


    def cell_parity(board):
        return len(board._player_cells(PlayerColor.RED)) - len(board._player_cells(PlayerColor.BLUE))

    return a1 * power_parity(board) + a2 * cell_parity(board)
def generate_valid_spawn_actions(board) -> list[Action]:
    """
    Generate a list of valid spawn actions. Defined as all cells not currently occupied.
    """
    if board._total_power >= BOARD_N ** 2:
        return []
    all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
    available_cells = [cell for cell in all_cells if not board._cell_occupied(cell)]
    return [SpawnAction(cell) for cell in available_cells]
def generate_valid_spread_actions(board, color) -> list[Action]:
    """
    Generate a list of valid spread actions. Defined all 6 directions for every cell owned by the player.
    """
    all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
    colored_cells = [cell for cell in all_cells if board[cell].player == color]
    return [SpreadAction(cell, direction) for cell in colored_cells for direction in HexDir]
def generate_valid_child_boards(parent_board: OurBoard, maximizing_player) -> list[OurBoard]:
    """
    Generate a list of valid child boards.
    """
    color = PlayerColor.RED if maximizing_player else PlayerColor.BLUE

    actions = generate_valid_spread_actions(parent_board, color) + generate_valid_spawn_actions(parent_board)

    for action in actions:
        new_board = parent_board.copy()
        new_board.apply_action(action)
        yield new_board
def generate_valid_child_boards_new(parent_board: OurBoard, maximizing_player) -> list[OurBoard]:
    def stack_ratio(board, color):
        all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
        colored_cells = [cell for cell in all_cells if board[cell].player == color]
        return board._color_power(color) / len(colored_cells)

    color = PlayerColor.RED if maximizing_player else PlayerColor.BLUE

    spread_actions = generate_valid_spread_actions(parent_board, color)

    spread_boards = []
    for action in spread_actions:
         new_board = parent_board.copy()
         new_board.apply_action(action)
         spread_boards.append((new_board, stack_ratio(new_board, color)))

    spread_boards.sort(key=lambda x: x[1], reverse=True)
    spread_boards = list(map(lambda x: x[0], spread_boards))


    spawn_actions = generate_valid_spawn_actions(parent_board)

    spawn_boards = []
    for action in spawn_actions:
        new_board = parent_board.copy()
        new_board.apply_action(action)
        spawn_boards.append(new_board)


    return spread_boards + spawn_boards
def minimax(board, depth, alpha, beta, maximizing_player, eval_func="default"):
    """
    Minimax algorithm with alpha-beta pruning.
    """
    if depth == 0 or board.game_over:
        if eval_func == "default":
            return evaluate_board(board, 10, 12), board, depth
        else:
            a1 = 0
            a2 = 1
            return evaluate_board(board, a1, a2), board, depth

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

if __name__ == "__main__":
    board = OurBoard(
        {
            HexPos(0, 0): CellState(PlayerColor.RED, 1),
            HexPos(2, 0): CellState(PlayerColor.BLUE, 1),
            HexPos(3, 0): CellState(PlayerColor.BLUE, 1),
            HexPos(4, 0): CellState(PlayerColor.BLUE, 1),
            HexPos(5, 0): CellState(PlayerColor.RED, 1),
            HexPos(6, 0): CellState(PlayerColor.RED, 1),
            HexPos(1, 1): CellState(PlayerColor.RED, 2),
            HexPos(0, 2): CellState(PlayerColor.RED, 1),
            HexPos(4, 6): CellState(PlayerColor.BLUE, 1),
        }
    )
    print(board.render(True))

    board._turn_color = PlayerColor.BLUE
    value, board_new, depth = minimax(board, 3, -100000000000, 100000000000, False)
    randocalc = 1 + 1
    print(randocalc)
# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, Board, BOARD_N


class GreedyAgent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self.board = Board()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def generate_valid_spawn_actions(self) -> list[SpawnAction]:
        """
        Generate all valid spawn actions. Defined as all cells that are not occupied.
        """
        if self.board._total_power >= BOARD_N ** 2:
            return []

        all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
        available_cells = [cell for cell in all_cells if not self.board._cell_occupied(cell)]
        return [SpawnAction(cell) for cell in available_cells]

    def generate_valid_spread_actions(self) -> list[SpreadAction]:
        """
        Generate all valid spread actions.
        Defined as a SpreadAction in every HexDir for every cell that is occupied by the current agent.
        """
        all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
        colored_cells = [cell for cell in all_cells if self.board[cell].player == self._color]
        return [SpreadAction(cell, direction) for cell in colored_cells for direction in HexDir]

    def rate_actions(self, actions: list[Action]):
        """
        Rate all actions based on the following criteria:
        - SpawnAction: The probability of the new spawn cell being covered by the opponent in the next iteration,
            where this probability is defined as the number of different actions the opponent can take to
            cover the cell divided by the total number of actions the opponent can take.
        - SpreadAction: The number of opponent's cells that will be captured by the spread action.

        Return two lists of tuples, where the first list contains the SpawnActions and the second list contains the
        SpreadActions. Each tuple contains the action and its rating.

        The lists are sorted in descending order based on the rating.
        """
        def rate_action(action: Action):
            match action:

                case SpawnAction(cell):
                    # Return the probability of the new spawn cell being covered by the opponent in the next iteration,
                    # where this probability is defined as the number of different actions the opponent can take to
                    # cover the cell divided by the total number of actions the opponent can take.
                    all_cells = [HexPos(r, q) for q in range(BOARD_N) for r in range(BOARD_N)]
                    opponent_cells = [cell for cell in all_cells if self.board[cell].player != self._color]

                    possible_action = 0
                    for opponent_cell in opponent_cells:
                        for direction in HexDir:
                            for i in range(self.board[opponent_cell].power):
                                if cell == opponent_cell + direction * (i + 1):
                                    possible_action += 1

                    return possible_action / len(opponent_cells) * len(HexDir)

                case SpreadAction(cell, direction):
                    # Return the number of opponent's cells that will be captured by the spread action.
                    to_cells = [
                        cell + direction * (i + 1) for i in range(self.board[cell].power)
                    ]

                    captured = 0
                    for cell in to_cells:
                        if self.board._cell_occupied(cell) and self.board[cell].player != self._color:
                            captured += 1

                    return captured

        spawn_actions_rated = [(rate_action(action), action) for action in actions if isinstance(action, SpawnAction)]
        spawn_actions_rated.sort(key=lambda x: x[0], reverse=True)
        print(f'Top-3 spawn actions: {spawn_actions_rated[:3]}')

        spread_actions_rated = [(rate_action(action), action) for action in actions if isinstance(action, SpreadAction)]
        spread_actions_rated.sort(key=lambda x: x[0], reverse=True)
        print(f'Top-3 spread actions: {spread_actions_rated[:3]}')

        return spawn_actions_rated, spread_actions_rated

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        # If there are no cells of the player on board, spawn a new cell
        if self.board._color_power(self._color) == 0:
            return random.choice(self.generate_valid_spawn_actions())

        # There are no legal spawn actions according to the rules
        if self.board._total_power >= BOARD_N ** 2:
            action = 'spread'

        # if there are too many cells of the player on board, spread a cell - spawn a cell will not be the best choice
        elif self.board._color_power(self._color) >= (BOARD_N ** 2) / 2:
            action = 'spread'

        # otherwise, randomly choose between spawn and spread
        else:
            action = random.choice(['spawn', 'spread'])

        best_actions = []
        match action:
            case 'spawn':
                actions = self.generate_valid_spawn_actions()
                spawn_rated_actions, _ = self.rate_actions(actions)

                best_actions = [action for score, action in spawn_rated_actions if score == spawn_rated_actions[0][0]]

            case 'spread':
                actions = self.generate_valid_spread_actions()
                _, spread_rated_actions = self.rate_actions(actions)

                best_actions = [action for score, action in spread_rated_actions if score == spread_rated_actions[0][0]]

        return best_actions[0]

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                self.board.apply_action(action)
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.apply_action(action)
                pass

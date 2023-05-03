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
    def generate_valid_spawn_actions(self) -> list[SpawnAction]:
        """
        Generate all valid spawn actions. Defined as all cells that are not occupied.
        """
        if self.board._total_power >= BOARD_N * 2:
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

    def rate_actions(self, actions: list[Action]) -> list[tuple[int, Action]]:
        """
        Evaluate the move and return a score.
        Only two things considered here:
            (1) is the Spawn action adjacent to opponents cell? -> -1 score, otherwise 0 score
            (2) is the Spread action capturing any opponents' cell? -> +1 score for each captured cell

        The resulting list is sorted in ascending order of score.
        """
        def rate_action(action: Action):
            match action:
                case SpawnAction(cell):
                    # We don't care as long as it is not directly next to an opponents' cell
                    for direction in HexDir:
                        neighbour = cell + direction
                        if self.board._cell_occupied(neighbour) and self.board[neighbour].player != self._color:
                            return -1
                    return 0
                case SpreadAction(cell, direction):
                    # We want to spread to capture as my of the pieces as possible
                    k = self.board[cell].power
                    captured = 0
                    for i in range(1, k + 1):
                        neighbour = cell + direction * i
                        if self.board._cell_occupied(neighbour) and self.board[neighbour].player != self._color:
                            captured += 1
                    return captured

        rated_actions = [(rate_action(action), action) for action in actions]
        rated_actions.sort(key=lambda x: x[0], reverse=True)

        print("Top 3 rated actions:" + str(rated_actions[:3]))

        return rated_actions

    def generate_valid_actions(self) -> list[Action]:
        """
        Generate all valid Actions (SpawnAction and SpreadAction).
        """
        return self.generate_valid_spawn_actions() + self.generate_valid_spread_actions()

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self.board._color_power(self._color) == 0:
            return random.choice(self.generate_valid_spawn_actions())
        else:
            actions = self.generate_valid_actions()
            rated_actions = self.rate_actions(actions)
            best_actions = [action for score, action in rated_actions if score == rated_actions[0][0]]
            return random.choice(best_actions)

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

# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir, Board


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class RandomAgent:
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

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        all_cells = [HexPos(r, q) for q in range(7) for r in range(7)]
        available_cells = [cell for cell in all_cells if not self.board._cell_occupied(cell)]
        if self.board._color_power(self._color) == 0:
            return SpawnAction(random.choice(available_cells))
        else:
            colored_cells = [cell for cell in all_cells if self.board[cell].player == self._color]
            actions = [SpreadAction(random.choice(colored_cells), random.choice(list(HexDir)))]
            if self.board._total_power < 49:
                actions.append(SpawnAction(random.choice(available_cells)))
            return random.choice(actions)

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

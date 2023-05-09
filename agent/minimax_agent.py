# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random

from agent.ourboard import OurBoard
from agent.minimax import minimax, generate_valid_spawn_actions
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexDir

class MinimaxAgent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self.board = OurBoard()
        self.maximizingPlayer = color == PlayerColor.RED
        self.minimax_depth = 3
        print(f"I am a {color} agent")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take. Runs minimax to find the best action.
        """
        if self.board._color_power(self._color) == 0:
            return random.choice(generate_valid_spawn_actions(self.board))
        else:
            value, board, depth = minimax(
                self.board,
                self.minimax_depth,
                -100000000000,
                100000000000,
                self.maximizingPlayer,
                eval_func="new"
            )
            best_action_depth = self.minimax_depth - depth
            best_action = board.last_ith_action(best_action_depth)
            print("Taking action with value", value)
            return best_action


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


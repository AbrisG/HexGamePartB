# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random

from agent.ourboard import OurBoard
from agent.minimax import minimax, generate_valid_spawn_actions
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexDir


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self.board = OurBoard()
        self.maximizingPlayer = color == PlayerColor.RED
        self.minimax_depth = 3

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self.board._color_power(self._color) == 0:
            return random.choice(generate_valid_spawn_actions(self.board))
        else:
            value, board, depth = minimax(
                self.board,
                self.minimax_depth,
                -100000000000,
                100000000000,
                self.maximizingPlayer
            )
            best_action_depth = self.minimax_depth - depth
            best_action = board.last_ith_action(best_action_depth)
            return best_action


    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        print(self.board._state)
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                self.board.apply_action(action)
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self.board.apply_action(action)
                pass



# Testing locally
if __name__ == "__main__":
    agent_red = Agent(PlayerColor.RED)
    agent_blue = Agent(PlayerColor.BLUE)

    print(agent_red.generate_valid_actions())
    action_red = agent_red.action()

    agent_red.turn(PlayerColor.RED, action_red)
    agent_blue.turn(PlayerColor.RED, action_red)

    action_blue_bad = SpawnAction(action_red.cell + HexDir.UpLeft)
    agent_blue.turn(PlayerColor.BLUE, action_blue_bad)
    agent_red.turn(PlayerColor.BLUE, action_blue_bad)

    action_red_good = agent_red.action()
    agent_red.turn(PlayerColor.RED, action_red_good)

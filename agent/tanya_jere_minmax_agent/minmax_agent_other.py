# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent
import random 

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from .minmax_other import MiniMax
from .gamestate_other import GameState

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class MiniMaxAgentOther:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state = GameState()
        self._game_turns = 0

        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self._game_turns == 0:
            return SpawnAction(HexPos(3, 3)) # doesn't matter where we spawn, every pos is the same

        minimax = MiniMax(self.color2char(self._color))
        
        #print(self._state)

        match self._color:
            case PlayerColor.RED:
                move = max(minimax.minimax_decision(self._state, 'r',0), key=lambda x:x[0])
                print("red", move)
                return move[1]
            case PlayerColor.BLUE:
                move = max(minimax.minimax_decision(self._state, 'b',0), key=lambda x:x[0])
                print("blue", move)
                return move[1]

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        self._state.apply_action(action, self.color2char(color))
        self._game_turns += 1

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass

    def color2char(self, color):
        if color == PlayerColor.BLUE: return 'b'
        if color == PlayerColor.RED: return 'r'

class RandomAgent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state = GameState()
        self._game_turns = 0

        match color:
            case PlayerColor.RED:
                print(f"Testing: I am playing as red {self._color}")
            case PlayerColor.BLUE:
                print(f"Testing: I am playing as blue {self._color}")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self._game_turns == 0:
            return SpawnAction(HexPos(3, 3)) # doesn't matter where we spawn, every pos is the same

        minimax = MiniMax(self.color2char(self._color))

        moves = minimax.find_possible_moves(self._state, self._color)

        #print(moves)

        return random.choice(moves)

        match self._color:
            case PlayerColor.RED:
                move = max(minimax.minimax_decision(self._state, 'r'))
                return move[1]
            case PlayerColor.BLUE:
                move = max(minimax.minimax_decision(self._state, 'r'))
                return move[1]

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        self._state.apply_action(action, self.color2char(color))
        self._game_turns += 1

        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass

    def color2char(self, color):
        if color == PlayerColor.BLUE: return 'b'
        if color == PlayerColor.RED: return 'r'
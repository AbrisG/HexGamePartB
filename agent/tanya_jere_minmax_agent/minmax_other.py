from copy import copy, deepcopy
import random
import math

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class MiniMax:
    def __init__(self, color) -> None:
        self._all_cells = set((x, y) for x in range(7) for y in range(7))    
        self._directions = (HexDir.Down, HexDir.Up, HexDir.UpLeft, HexDir.DownLeft, HexDir.DownRight, HexDir.UpRight)
        self._memo = dict()
        self._color = color # true player color
        self._depth = 0


    def find_possible_moves(self, state, color):
        cells = state.find_non_empty_cells()
        opponent_color = 'r' if color==PlayerColor.BLUE else 'b'
        our_color = 'r' if color==PlayerColor.RED else 'b'

        non_empty_cells = set()
        possible_moves = []
        #print(state, f'our color: {our_color}')
        for cell in cells[our_color]:
            non_empty_cells.add((cell[0],cell[1]))
            for dir in self._directions:
                possible_moves.append(SpreadAction(HexPos(cell[0],cell[1]),dir))

        for cell in cells[opponent_color]:
            non_empty_cells.add((cell[0],cell[1]))
        
        empty_cells = self._all_cells - non_empty_cells

        for empty in random.choices(list(empty_cells), k=5):
            possible_moves.append(SpawnAction(HexPos(empty[0],empty[1])))
        return possible_moves


    def minimax_decision(self, state, color, depth) -> list:
        possible_moves = self.find_possible_moves(state, color)
        #state_hash = hash(state)
        #self._memo[state_hash] 
        moves = []

        for move in random.choices(possible_moves, k=5):
            new_state = deepcopy(state)
            new_state.apply_action(move, color)
            moves.append((self.minimax_value(new_state, color, depth), move, depth))
        return moves


    def terminal_state_check(self, state, color):
        # TODO add 343 check
        cells = state.find_non_empty_cells()
        opponent_color = 'r' if color==PlayerColor.BLUE else 'b'
        our_color = 'r' if color==PlayerColor.RED else 'b'

        total_sum = 0
        for blue in cells['b']:
            total_sum += blue[2]
        for red in cells['r']:
            total_sum += red[2]

        if total_sum>49:
            return (True, False)

        if len(cells[opponent_color]) == 0:
            return (True, True)
        elif len(cells[our_color])==0:
            return (True, False)
        return (False, False)


    def utility_state_function(self, state, color) -> float:
        """
        returns a eval value for a given state
        """
        cells = state.find_non_empty_cells()

        power_value = 1.2

        utilitiy_value_state = 0
        if color == PlayerColor.BLUE:
            for value in cells['b']:
                utilitiy_value_state += value[2]**1.2
        else:
            for value in cells['r']:
                utilitiy_value_state += value[2]**1.2
        
        final_steps = state.heuristic('b' if color==PlayerColor.BLUE else 'r')
        
        #parameters:
        a=1
        b=2

        return a*utilitiy_value_state + b*(1/(-1 if final_steps==1 else final_steps))
    

    def minimax_value(self, state, color, depth):
        if depth>4:
            return self.utility_state_function(state, color)
        
        over, winner = self.terminal_state_check(state, color)
        if over:
            if winner:
                return 100
            return -100
        
        other_color = 'r' if color=='b' else 'b'

        res = self.minimax_decision(state, other_color, depth+1)
        if color == self._color:
            return min(res, key=lambda x:x[0])[0]
        else:
            return max(res, key=lambda x:x[0])[0]
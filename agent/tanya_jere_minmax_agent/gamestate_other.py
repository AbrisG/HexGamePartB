from copy import copy, deepcopy

from .utils import render_board
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class GameState:
    """
    This is the state class of the game board.
    The board is stored in a 2D array of lists.
    """
    _coordinate_system = dict()

    def __init__(self) -> None:
        self._coordinate_system = dict()

    def __str__(self) -> str:
        return render_board(self.convert_to_dict(), ansi=True)

    def __hash__(self) -> int:
        return hash(tuple(sorted(list(self._coordinate_system.items()))))
        
    def __lt__(self, other):
        return self.find_non_empty_cells()['r'] < other.find_non_empty_cells()['r']
    
    def __le__(self, other):
        return self.find_non_empty_cells()['r'] <= other.find_non_empty_cells()['r']

    def convert_to_dict(self) -> dict:
        return self._coordinate_system

    def at(self, r, q) -> tuple:
        if (r%7, q%7) not in self._coordinate_system:
            return ('e',0)
        return self._coordinate_system[(r%7, q%7)]
    
    def set(self, r, q, color, power):
        if color not in ['r','b','e']:
            raise Exception("Impossible color!")
        if power>6:
            self._coordinate_system.pop((r%7,q%7))
        elif color=='e':
            if (r%7,q%7) in self._coordinate_system:
                self._coordinate_system.pop((r%7,q%7))
        else:
            self._coordinate_system[(r%7,q%7)] = (color, power)
    
    def import_state(self, given_state):
        """
        loads the given state into the CoordinateSystem

        given_state: dict of state in the format of the class
        """
        _coordinate_system = dict()
        for key, value in given_state.items():
            self._coordinate_system[(key[0], key[1])] = value # r is first coordinate and q is second coordinate

    def import_state_list(self, given_state_list):
        self._coordinate_system = deepcopy(given_state_list)

    def export_state_list(self) -> list:
        return self._coordinate_system

    def find_non_empty_cells(self) -> dict:
        cells = dict()
        cells['r'] = []
        cells['b'] = []

        for key, item in self._coordinate_system.items():
            cells[item[0]].append((key[0], key[1], item[1])) # r, q, value
        return cells
    
    def apply_spread(self,r,q,d_r,d_q):
        """
        given a cell, apply a spread from (r,q) into the d_r and d_q direction
        """
        if (d_r,d_q) not in [(-1,1),(0,1),(1,0),(1,-1),(0,-1),(-1,0)]:
            raise Exception(f'Invalid spread direction!\n{(d_r,d_q)} is not possible!')

        current_cell = self.at(r,q)

        if current_cell[0] == 'e':
            raise Exception("Not possible to spread because empty cell!!")

        for i in range(current_cell[1]+1): # get the power of cell and spread into the direction according to given power
            new_cell = (r + d_r*i, q + d_q*i) 

            new_cell_state = self.at(new_cell[0],new_cell[1])

            self.set(new_cell[0], new_cell[1], current_cell[0], new_cell_state[1]+1)

        self.set(r, q, 'e', 0)
    
    def apply_action(self, action, color):
        if type(action)==SpawnAction:
            self.set(action.cell.r, action.cell.q, color, 1)
        elif type(action)==SpreadAction:
            self.apply_spread(action.cell.r, action.cell.q, action.direction.r, action.direction.q)

    def calculate_distance(self, r1, q1, r2, q2) -> int:
        tr = 3-r1
        tq = 3-q1
        r1 = (r1+tr)%7
        r2 = (r2+tr)%7
        q1 = (q1+tq)%7
        q2 = (q2+tq)%7

        if (r2,q2) in set([(0,0),(1,0),(0,1),(6,5),(5,6),(6,6)]):
            return 4

        return (abs(r1-r2)+abs(q1+r1-r2-q2)+abs(q1-q2))/2

    def calculate_distance_approx(self, r1, q1, r2, q2) -> int:
        # uses approximation:   
        return max(abs(r1-r2),abs(q1-q2))

    def heuristic(self, main_color, blue_count=False) -> int:
        nec = self.find_non_empty_cells()
        min_distance = 10000
        red_value = 1

        opponent_color = 'r' if main_color == 'b' else 'b'
        if len(nec[opponent_color])==0:
            return 0
        for red in nec[main_color]:
            for blue in nec[opponent_color]:
                if min_distance>self.calculate_distance(red[0],red[1], blue[0], blue[1]):
                    #min_distance = min(min_distance, self.calculate_distance(red[0],red[1], blue[0], blue[1]))
                    min_distance=self.calculate_distance(red[0],red[1], blue[0], blue[1])
                    red_value = red[2]

        if blue_count:
            return min_distance + len(nec[opponent_color])
        return min_distance if min_distance==1 else min_distance/red_value
    
    def blue_heuristic(self):
        # unused in Part A
        nec = self.find_non_empty_cells()
        blue_count = len(nec['b'])
        max_red = 0
        for red in nec['r']:
            max_red = max(max_red, red[2])

        return blue_count-max_red

    def percentage_heuristic(self):
        nec = self.find_non_empty_cells()
        r_power = 0
        b_power = 0
        for cell in nec['r']:
            r_power += cell[2]
        for cell in nec['b']:
            b_power += cell[2]

        return b_power / (r_power+b_power)
from referee.game import Board


class OurBoard(Board):


    def copy(self):
        b = OurBoard(self._state.copy())
        b._history = self._history.copy()
        b._turn_color = self._turn_color
        return b

    def last_ith_action(self, i):
        return self._history[-i].action

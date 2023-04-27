from referee.game import PlayerColor, HexDir, HexPos


class Position:
    def __init__(self, color: PlayerColor, state: dict):
        self._current_player = color
        self._next_player = color.opponent
        self._state = state

    def is_terminal(self):
        num_blue = list(filter(lambda x: x[1] == PlayerColor.BLUE, self._state.items()))
        num_red = list(filter(lambda x: x[1] == PlayerColor.RED, self._state.items()))
        return len(num_blue) == 0 or len(num_red) == 0

    # Red is considered to be the maximizing player
    def evaluate(self):
        num_blue = list(filter(lambda x: x[1] == PlayerColor.BLUE, self._state.items()))
        num_red = list(filter(lambda x: x[1] == PlayerColor.RED, self._state.items()))
        return len(num_red) - len(num_blue)

    def _spawn_permitted(self):
        sum_k = 0
        for vec in self._state:
            sum_k += self._state[vec][1]

        return sum_k < 49

    # TODO: Rewrite assuming key is HexPos
    def _spawn_children(self):
        all_vecs = {HexPos(r, q) for r in range(7) for q in range(7)}
        available_vecs = all_vecs- set(self._state.keys())
        children = []
        for vec in available_vecs:
            new_state = self._state.copy()
            new_state[vec] = (self._current_player, 1)
            children.append(Position(self._next_player, new_state))

        print("Generating SPAWN children: " + str(len(children)))
        return children

    def _spread_children(self):
        children = []

        relevant_vecs = list(filter(lambda x: x[1][0] == self._current_player, self._state.items()))

        for vec, info in relevant_vecs:
            new_state = self._state.copy()
            del new_state[vec]
            k = info[1]

            for direction in HexDir:
                for i in range(1, k + 1):
                    new_vec = vec + direction * i
                    new_k = new_state[new_vec][1] + 1 if new_vec in new_state else 1
                    if new_k > 6:
                        del new_state[new_vec]
                    else:
                        new_state[new_vec] = (self._current_player, new_k)
                children.append(Position(self._next_player, new_state))

        print("Generating SPREAD children: " + str(len(children)))
        return children

    def get_children(self):
        children = []

        # Spawn
        if self._spawn_permitted():
            children.extend(self._spawn_children())

        # Spread
        children.extend(self._spread_children())

        return children


def minimax(position, depth, color: PlayerColor):
    if depth == 0 or position.is_terminal():
        return position.evaluate()

    if color == PlayerColor.RED:
        max_eval = -100000
        for child in position.get_children():
            eval = minimax(child, depth - 1, PlayerColor.BLUE)
            max_eval = max(max_eval, eval)
        return max_eval

    else:
        min_eval = 100000
        for child in position.get_children():
            eval = minimax(child, depth - 1, PlayerColor.RED)
            min_eval = min(min_eval, eval)
        return min_eval



pos = Position(PlayerColor.RED, {HexPos(3, 3): (PlayerColor.RED, 1)})
pos.get_children()
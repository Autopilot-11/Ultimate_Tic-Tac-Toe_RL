"""An exact minimax agent for ordinary Tic-Tac-Toe."""

from src.g0.game import Board, EMPTY


class MinimaxAgent:
    def __init__(self):
        self.cache: dict[tuple[tuple[int, ...], int, int], int] = {}

    def select_action(self, game: Board) -> int:
        """Return the optimal legal action for the current player."""
        action_values = self.evaluate_actions(game)
        return max(action_values, key=action_values.get)

    def evaluate_actions(self, game: Board) -> dict[int, int]:
        """Return the minimax value of each legal action for the current player."""
        if game.is_terminal():
            raise ValueError("Game has already ended")

        maximizing_player = game.current_player
        action_values = {}
        for action in game.legal_actions():
            child = game.clone()
            child.apply_action(action)
            action_values[action] = self._minimax_value(child, maximizing_player)

        return action_values

    def _minimax_value(self, game: Board, maximizing_player: int) -> int:
        """Return the value of game from maximizing_player's perspective."""
        state_key = (
            tuple(game.board),
            game.current_player,
            maximizing_player,
        )

        if state_key in self.cache:
            return self.cache[state_key]

        if game.is_terminal():
            winner = game.winner()
            if winner == EMPTY:
                value = 0
            elif winner == maximizing_player:
                value = 1
            else:
                value = -1
            self.cache[state_key] = value
            return value

        values = []
        for action in game.legal_actions():
            child = game.clone()
            child.apply_action(action)
            values.append(self._minimax_value(child, maximizing_player))

        if game.current_player == maximizing_player:
            value = max(values)
        else:
            value = min(values)

        self.cache[state_key] = value
        return value

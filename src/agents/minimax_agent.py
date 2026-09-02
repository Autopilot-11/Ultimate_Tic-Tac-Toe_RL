"""An exact minimax agent for ordinary Tic-Tac-Toe."""

from src.g0.game import Board, EMPTY, X, O

class MinimaxAgent:
    def select_action(self, game:Board) -> int:
        """Return the optimal legal action for the current player."""

        if game.is_terminal():
            raise ValueError("Game has already ended")
        
        # Initialize
        maximizing_player = game.current_player
        best_value = -float("inf")
        best_action = None

        for action in game.legal_actions():
            copy = game.clone()
            copy.apply_action(action)
            value = self._minimax_value(copy, game.current_player)
            if value > best_value:
                best_value = value
                best_action = action

        return best_action
        

    def _minimax_value(self, game: Board, maximizing_player: int) -> int:
        """Return the value of game from maximizing_player's perspective."""
        winner = game.winner()

        if game.is_terminal():
            if winner == EMPTY:
                return 0
            if winner == maximizing_player:
                return 1
            return -1
        else:
            values = []
            for action in game.legal_actions():
                child = game.clone()
                child.apply_action(action)
                values.append(self._minimax_value(child,maximizing_player))
            if game.current_player == maximizing_player:
                return max(values)
            return min(values)


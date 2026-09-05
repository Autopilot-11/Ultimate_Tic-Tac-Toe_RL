"""A Monte Carlo rollout baseline for deterministic two-player games."""

import random

from src.g0.game import EMPTY


class RolloutAgent:
    """Estimate an action's value from random completions of its child state."""

    def __init__(self, num_rollouts: int = 50, seed: int | None = None):
        if num_rollouts < 1:
            raise ValueError("num_rollouts must be at least 1.")

        self.num_rollouts = num_rollouts
        self.rng = random.Random(seed)

    def select_action(self, game) -> int:
        """Return a legal action with the highest estimated rollout value."""
        action_values = self.evaluate_actions(game)
        best_value = max(action_values.values())
        best_actions = [
            action for action, value in action_values.items() if value == best_value
        ]
        return self.rng.choice(best_actions)

    def evaluate_actions(self, game) -> dict[int, float]:
        """Estimate every legal action's value from the current player's view."""
        if game.is_terminal():
            raise ValueError("Cannot select an action in a terminal game.")

        root_player = game.current_player
        action_values = {}
        for action in game.legal_actions():
            total_return = 0

            for _ in range(self.num_rollouts):
                child = game.clone()
                child.apply_action(action)
                total_return += self._rollout_return(child, root_player)

            action_values[action] = total_return / self.num_rollouts

        return action_values

    def _rollout_return(self, game, root_player: int) -> int:
        """Play randomly to a terminal state and return +1, 0, or -1."""
        while not game.is_terminal():
            action = self.rng.choice(game.legal_actions())
            game.apply_action(action)

        winner = game.winner()
        if winner == EMPTY:
            return 0
        return 1 if winner == root_player else -1

"""A lightweight tactical baseline for Ultimate Tic-Tac-Toe."""

import random

from src.g0.game import EMPTY
from src.g1.game import UBoard


class HeuristicAgent:
    """Choose moves using immediate tactical wins and blocks.

    The numeric scores are priorities, not learned values. A global win is much
    more important than a local-board win, and allowing an opponent global win
    is strongly penalized.
    """

    GLOBAL_WIN = 10_000
    LOCAL_WIN = 100
    OPPONENT_GLOBAL_WIN = 1_000
    OPPONENT_LOCAL_WIN = 10

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def select_action(self, game: UBoard) -> int:
        """Return a highest-scoring legal action, breaking ties randomly."""
        action_scores = self.evaluate_actions(game)
        best_score = max(action_scores.values())
        best_actions = [
            action for action, score in action_scores.items() if score == best_score
        ]
        return self.rng.choice(best_actions)

    def evaluate_actions(self, game: UBoard) -> dict[int, int]:
        """Return tactical scores for every legal action in game."""
        if game.is_terminal():
            raise ValueError("Cannot select an action in a terminal game.")

        player = game.current_player
        action_scores = {}

        for action in game.legal_actions():
            child = game.clone()
            local_board = action // 9
            child.apply_action(action)

            if child.winner() == player:
                action_scores[action] = self.GLOBAL_WIN
                continue

            score = 0
            if child.local_winners[local_board] == player:
                score += self.LOCAL_WIN

            opponent_global_wins, opponent_local_wins = self._immediate_wins(child)
            score -= self.OPPONENT_GLOBAL_WIN * opponent_global_wins
            score -= self.OPPONENT_LOCAL_WIN * opponent_local_wins
            action_scores[action] = score

        return action_scores

    def _immediate_wins(self, game: UBoard) -> tuple[int, int]:
        """Count the current player's global and local wins available in one move."""
        player = game.current_player
        global_wins = 0
        local_wins = 0

        for action in game.legal_actions():
            child = game.clone()
            local_board = action // 9
            child.apply_action(action)

            if child.winner() == player:
                global_wins += 1
            elif child.local_winners[local_board] == player:
                local_wins += 1

        return global_wins, local_wins

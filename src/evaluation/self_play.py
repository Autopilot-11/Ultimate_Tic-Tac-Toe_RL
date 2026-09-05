"""Reusable self-play evaluation utilities for G0 and G1."""

from src.agents.random_agent import RandomAgent
from src.g0.game import Board, EMPTY, O, X
from src.g1.game import UBoard


def play_game(x_agent, o_agent, game_factory=Board) -> int:
    """Play one complete game created by game_factory and return its winner."""
    game = game_factory()

    while not game.is_terminal():
        agent = x_agent if game.current_player == X else o_agent
        action = agent.select_action(game)
        game.apply_action(action)
    return game.winner()


def run_match(x_agent, o_agent, num_games: int, game_factory=Board) -> dict[int, int]:
    """Run num_games games and return counts keyed by winner."""
    results = {X: 0, O: 0, EMPTY: 0}

    for _ in range(num_games):
        winner = play_game(x_agent, o_agent, game_factory)
        results[winner] += 1

    return results


def run_side_swapped_match(agent_a, agent_b, games_per_side: int, game_factory=Board) -> dict[str, int]:
    """Evaluate two agents equally often as X and O.

    The returned win counts belong to agents, rather than board symbols, so a
    first-player advantage does not get mistaken for agent strength.
    """
    results = {"agent_a_wins": 0, "agent_b_wins": 0, "draws": 0}

    for x_agent, o_agent, agent_a_player in (
        (agent_a, agent_b, X),
        (agent_b, agent_a, O),
    ):
        for _ in range(games_per_side):
            winner = play_game(x_agent, o_agent, game_factory)
            if winner == EMPTY:
                results["draws"] += 1
            elif winner == agent_a_player:
                results["agent_a_wins"] += 1
            else:
                results["agent_b_wins"] += 1

    return results


def run_random_self_play(num_games: int = 1_000) -> dict[int, int]:
    """Run the existing seeded random G0 baseline."""
    return run_match(RandomAgent(seed=0), RandomAgent(seed=1), num_games)


def run_random_g1_self_play(num_games: int = 1_000) -> dict[int, int]:
    """Run seeded random self-play games in Ultimate Tic-Tac-Toe."""
    return run_match(RandomAgent(seed=0), RandomAgent(seed=1), num_games, UBoard)

if __name__ == "__main__":
    results = run_random_self_play()
    print(f"X wins: {results[X]}")
    print(f"O wins: {results[O]}")
    print(f"Draws: {results[EMPTY]}")

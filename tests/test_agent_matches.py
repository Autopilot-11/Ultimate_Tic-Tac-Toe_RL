"""Behavioral tests for G0 agents playing complete games."""

from src.agents.minimax_agent import MinimaxAgent
from src.agents.random_agent import RandomAgent
from src.evaluation.self_play import play_game, run_match
from src.g0.game import EMPTY, O, X


def test_minimax_never_loses_to_random_as_x():
    minimax = MinimaxAgent()

    for seed in range(10):
        winner = play_game(minimax, RandomAgent(seed=seed))
        assert winner != O


def test_minimax_never_loses_to_random_as_o():
    minimax = MinimaxAgent()

    for seed in range(10):
        winner = play_game(RandomAgent(seed=seed), minimax)
        assert winner != X


def test_minimax_draws_against_itself():
    assert play_game(MinimaxAgent(), MinimaxAgent()) == EMPTY


def test_run_match_records_every_game():
    results = run_match(RandomAgent(seed=0), RandomAgent(seed=1), num_games=25)

    assert set(results) == {X, O, EMPTY}
    assert sum(results.values()) == 25

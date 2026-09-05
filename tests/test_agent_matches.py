"""Behavioral tests for G0 agents playing complete games."""

from src.agents.minimax_agent import MinimaxAgent
from src.agents.heuristic_agent import HeuristicAgent
from src.agents.random_agent import RandomAgent
from src.agents.rollout_agent import RolloutAgent
from src.evaluation.self_play import (
    play_game,
    run_match,
    run_random_g1_self_play,
    run_side_swapped_match,
)
from src.g0.game import EMPTY, O, X
from src.g1.game import UBoard


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


def test_random_g1_self_play_completes_every_game():
    results = run_random_g1_self_play(num_games=100)

    assert set(results) == {X, O, EMPTY}
    assert sum(results.values()) == 100


def test_heuristic_agent_takes_an_immediate_global_win():
    game = UBoard()
    game.local_winners[0:2] = [X, X]
    game.board[18:27] = [X, X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    game.forced_board = 2
    game.current_player = X

    assert HeuristicAgent(seed=0).select_action(game) == 20


def test_heuristic_agent_takes_an_immediate_local_win():
    game = UBoard()
    game.board[0:9] = [X, X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    game.forced_board = 0
    game.current_player = X

    assert HeuristicAgent(seed=0).select_action(game) == 2


def test_heuristic_agent_can_complete_g1_games_against_random():
    results = run_match(
        HeuristicAgent(seed=0), RandomAgent(seed=1), num_games=20, game_factory=UBoard
    )

    assert sum(results.values()) == 20


def test_side_swapped_evaluation_counts_both_starting_positions():
    results = run_side_swapped_match(
        RandomAgent(seed=0), RandomAgent(seed=1), games_per_side=10, game_factory=UBoard
    )

    assert set(results) == {"agent_a_wins", "agent_b_wins", "draws"}
    assert sum(results.values()) == 20


def test_rollout_agent_returns_a_legal_g1_action():
    game = UBoard()
    agent = RolloutAgent(num_rollouts=3, seed=0)

    assert agent.select_action(game) in game.legal_actions()


def test_rollout_agent_takes_an_immediate_global_win():
    game = UBoard()
    game.local_winners[0:2] = [X, X]
    game.board[18:27] = [X, X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    game.forced_board = 2
    game.current_player = X

    assert RolloutAgent(num_rollouts=3, seed=0).select_action(game) == 20


def test_rollout_agent_can_complete_a_g1_game_against_random():
    results = run_match(
        RolloutAgent(num_rollouts=2, seed=0),
        RandomAgent(seed=1),
        num_games=1,
        game_factory=UBoard,
    )

    assert sum(results.values()) == 1

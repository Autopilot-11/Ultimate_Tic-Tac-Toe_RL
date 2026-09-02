"""Tests for the Ultimate Tic-Tac-Toe environment."""

import pytest

from src.g0.game import EMPTY, O, X
from src.g1.game import UBoard


def test_new_game_allows_every_action():
    game = UBoard()

    assert game.current_player == X
    assert game.forced_board is None
    assert game.legal_actions() == list(range(81))


def test_action_routes_opponent_to_the_selected_local_cell():
    game = UBoard()
    game.apply_action(43)  # Local board 4, local cell 7.

    assert game.board[43] == X
    assert game.current_player == O
    assert game.forced_board == 7
    assert game.legal_actions() == list(range(63, 72))


def test_completed_target_board_releases_the_forced_board_constraint():
    game = UBoard()
    game.local_complete[7] = True
    game.apply_action(43)  # Local cell 7 would normally force board 7.

    assert game.forced_board is None
    assert 63 not in game.legal_actions()
    assert 0 in game.legal_actions()


def test_winner_for_cells_checks_the_requested_local_board():
    game = UBoard()
    game.board[9:18] = [O, O, O, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]

    assert game.winner_for_cells(1) == O
    assert game.winner_for_cells(0) == EMPTY


def test_local_and_global_winners_are_detected():
    game = UBoard()
    game.board[0:9] = [X, X, X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    game._update_local_status(0)
    game.local_winners[1] = X
    game.local_winners[2] = X

    assert game.local_winners[0] == X
    assert game.local_complete[0]
    assert game.winner() == X
    assert game.is_terminal()


def test_clone_is_independent():
    game = UBoard()
    game.apply_action(0)
    cloned_game = game.clone()
    game.apply_action(1)

    assert cloned_game.board[1] == EMPTY
    assert cloned_game.current_player == O


def test_illegal_actions_raise_errors():
    game = UBoard()
    game.apply_action(0)

    with pytest.raises(ValueError):
        game.apply_action(0)

    with pytest.raises(ValueError):
        game.apply_action(9)

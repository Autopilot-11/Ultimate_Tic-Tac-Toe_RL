"""Tests for the ordinary Tic-Tac-Toe environment."""

import pytest

from src.g0.game import EMPTY, O, X, Board


def test_new_game_has_all_moves_available():
    game = Board()

    assert game.board == [EMPTY] * 9
    assert game.current_player == X
    assert game.legal_actions() == list(range(9))
    assert not game.is_terminal()


def test_apply_action_places_mark_and_switches_player():
    game = Board()
    game.apply_action(4)

    assert game.board[4] == X
    assert game.current_player == O
    assert 4 not in game.legal_actions()


def test_cannot_play_an_occupied_or_out_of_range_cell():
    game = Board()
    game.apply_action(0)

    with pytest.raises(ValueError):
        game.apply_action(0)

    with pytest.raises(ValueError):
        game.apply_action(9)


def test_winner_detects_a_completed_line_before_board_is_full():
    game = Board()
    game.board = [X, X, X, O, EMPTY, O, EMPTY, EMPTY, EMPTY]

    assert game.winner() == X
    assert game.is_terminal()


def test_full_board_without_winner_is_a_draw():
    game = Board()
    game.board = [X, O, X, X, O, O, O, X, X]

    assert game.winner() == EMPTY
    assert game.is_terminal()


def test_full_board_can_still_have_a_winner():
    game = Board()
    game.board = [X, X, X, O, O, X, O, X, O]

    assert game.winner() == X
    assert game.is_terminal()

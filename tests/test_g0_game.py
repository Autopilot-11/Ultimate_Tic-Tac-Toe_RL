"""Tests for the ordinary Tic-Tac-Toe environment."""

import pytest

from src.g0.game import EMPTY, O, WINNING_LINES, X, Board


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

    with pytest.raises(ValueError):
        game.apply_action(-1)


@pytest.mark.parametrize("winning_line", WINNING_LINES)
@pytest.mark.parametrize("player", (X, O))
def test_winner_detects_every_winning_line(winning_line, player):
    game = Board()
    for cell in winning_line:
        game.board[cell] = player

    assert game.winner() == player
    assert game.is_terminal()


def test_game_has_no_legal_actions_after_a_win():
    game = Board()
    game.board = [X, X, X, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]

    assert game.legal_actions() == []
    with pytest.raises(ValueError):
        game.apply_action(3)


def test_clone_board_function():
    game = Board()
    game.board = [X, X, EMPTY, EMPTY, O, EMPTY, EMPTY, EMPTY, EMPTY]
    game.current_player = O
    new_board = game.clone()
    game.apply_action(3)

    assert game.board == [X, X, EMPTY, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    assert new_board.board == [X, X, EMPTY, EMPTY, O, EMPTY, EMPTY, EMPTY, EMPTY]


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


def test_render_returns_a_readable_board():
    game = Board()
    game.board = [X, O, EMPTY, EMPTY, X, EMPTY, EMPTY, EMPTY, O]

    assert game.render() == "X | O |  \n---------\n  | X |  \n---------\n  |   | O"

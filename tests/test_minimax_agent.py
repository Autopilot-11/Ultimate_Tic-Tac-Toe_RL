"""Tests for the exact G0 minimax agent."""

import pytest

from src.agents.minimax_agent import MinimaxAgent
from src.g0.game import EMPTY, O, X, Board


def test_minimax_chooses_an_immediate_winning_move():
    game = Board()
    game.board = [X, X, EMPTY, O, O, EMPTY, EMPTY, EMPTY, EMPTY]
    game.current_player = X

    assert MinimaxAgent().select_action(game) == 2


def test_minimax_blocks_an_opponents_immediate_winning_move():
    game = Board()
    game.board = [O, O, EMPTY, X, EMPTY, EMPTY, X, EMPTY, EMPTY]
    game.current_player = X

    assert MinimaxAgent().select_action(game) == 2


def test_minimax_rejects_terminal_games():
    game = Board()
    game.board = [X, X, X, O, O, EMPTY, EMPTY, EMPTY, EMPTY]

    with pytest.raises(ValueError):
        MinimaxAgent().select_action(game)

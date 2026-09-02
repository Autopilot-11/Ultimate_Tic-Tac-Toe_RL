"""Game rules and state transitions for Ultimate Tic-Tac-Toe (G1)."""

from src.g0.game import EMPTY, O, WINNING_LINES, X


class UBoard:
    """A mutable Ultimate Tic-Tac-Toe game state.

    Actions use a flattened encoding from 0 through 80:
    ``action = local_board * 9 + local_cell``.
    """

    def __init__(self):
        self.board = [EMPTY] * 81
        self.current_player = X
        self.local_winners = [EMPTY] * 9
        self.local_complete = [False] * 9
        self.forced_board: int | None = None

    def is_legal_move(self, action: int) -> bool:
        """Return whether an action obeys both occupancy and routing rules."""
        if not 0 <= action < 81 or self.is_terminal() or self.board[action] != EMPTY:
            return False

        local_board = action // 9
        if self.local_complete[local_board]:
            return False

        return self.forced_board is None or local_board == self.forced_board

    def legal_actions(self) -> list[int]:
        """Return all actions allowed by the current forced-board constraint."""
        if self.is_terminal():
            return []

        if self.forced_board is not None:
            start = self.forced_board * 9
            return [
                action
                for action in range(start, start + 9)
                if self.is_legal_move(action)
            ]

        return [action for action in range(81) if self.is_legal_move(action)]

    def apply_action(self, action: int) -> None:
        """Apply a legal move, update local results, and route the next player."""
        if not self.is_legal_move(action):
            raise ValueError(f"Illegal action: {action}")

        local_board = action // 9
        local_cell = action % 9
        self.board[action] = self.current_player
        self._update_local_status(local_board)

        # The local cell selected determines the opponent's target local board.
        self.forced_board = None if self.local_complete[local_cell] else local_cell
        self.current_player *= -1

    def clone(self) -> "UBoard":
        """Return an independent copy for planning and simulations."""
        copied_game = UBoard()
        copied_game.board = self.board.copy()
        copied_game.current_player = self.current_player
        copied_game.local_winners = self.local_winners.copy()
        copied_game.local_complete = self.local_complete.copy()
        copied_game.forced_board = self.forced_board
        return copied_game

    def winner_for_cells(self, local_board: int) -> int:
        """Return the winner of one local 3x3 board, or EMPTY if none exists."""
        start = local_board * 9
        cells = self.board[start : start + 9]

        for a, b, c in WINNING_LINES:
            if cells[a] == cells[b] == cells[c] != EMPTY:
                return cells[a]

        return EMPTY

    def winner(self) -> int:
        """Return the player that won the global 3x3 grid of local boards."""
        for a, b, c in WINNING_LINES:
            if (
                self.local_winners[a]
                == self.local_winners[b]
                == self.local_winners[c]
                != EMPTY
            ):
                return self.local_winners[a]

        return EMPTY

    def is_terminal(self) -> bool:
        """Return True after a global win or when every local board is complete."""
        return self.winner() != EMPTY or all(self.local_complete)

    def render(self) -> str:
        """Return a readable 9x9 terminal rendering with local-board separators."""
        symbols = {X: "X", O: "O", EMPTY: " "}
        rows = []

        for global_row in range(3):
            for local_row in range(3):
                groups = []
                for global_column in range(3):
                    local_board = global_row * 3 + global_column
                    start = local_board * 9 + local_row * 3
                    groups.append(" | ".join(symbols[cell] for cell in self.board[start : start + 3]))
                rows.append(" || ".join(groups))
            if global_row < 2:
                rows.append("=========++=========++=========")

        return "\n".join(rows)

    def _update_local_status(self, local_board: int) -> None:
        """Mark a local board complete after a win or a full-board draw."""
        local_winner = self.winner_for_cells(local_board)
        start = local_board * 9
        cells = self.board[start : start + 9]

        if local_winner != EMPTY:
            self.local_winners[local_board] = local_winner
            self.local_complete[local_board] = True
        elif not any(cell == EMPTY for cell in cells):
            self.local_complete[local_board] = True

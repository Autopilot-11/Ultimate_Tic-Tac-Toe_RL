"""Game rules and state transitions for ordinary Tic-Tac-Toe."""

EMPTY = 0
X = 1
O = -1

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class Board:
    """ A mutable ordinary Tic-Tac-Toe board."""

    def __init__(self):
        self.board = [EMPTY] * 9
        self.current_player = X

    def is_legal_move(self, action: int) -> bool:
        """Return whether action names an empty cell on the board."""
        return 0 <= action < 9 and self.board[action] == EMPTY and not self.is_terminal()

    def apply_action(self, action: int) -> None:
        """Place the current player's mark, then pass the turn to the opponent."""
        if not self.is_legal_move(action):
            raise ValueError(f"Illegal action: {action}")

        self.board[action] = self.current_player
        self.current_player *= -1

    def legal_actions(self) -> list[int]:
        """Return every board index that may be played next."""
        return [action for action in range(9) if self.is_legal_move(action)]

    def winner(self) -> int:
        """Return X or O if that player has won; otherwise return EMPTY."""
        for a, b, c in WINNING_LINES:
            if self.board[a] == self.board[b] == self.board[c] != EMPTY:
                return self.board[a]

        return EMPTY

    def is_terminal(self) -> bool:
        """Return True when the game has ended in a win or a full-board draw."""
        return self.winner() != EMPTY or not any(cell == EMPTY for cell in self.board)

    def render(self) -> str:
        """Return a compact text representation for debugging in the terminal."""
        symbols = {X: "X", O: "O", EMPTY: " "}
        rows = []
        for start in range(0, 9, 3):
            row = self.board[start : start + 3]
            rows.append(" | ".join(symbols[cell] for cell in row))
        return "\n---------\n".join(rows)

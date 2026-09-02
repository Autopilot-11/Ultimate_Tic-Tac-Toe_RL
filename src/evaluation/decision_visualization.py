"""Terminal tools for inspecting an agent's minimax decisions."""

from src.agents.minimax_agent import MinimaxAgent
from src.g0.game import Board, EMPTY, O, X


def render_action_values(
    game: Board, action_values: dict[int, int], selected_action: int
) -> str:
    """Render board squares with action-value labels and the selected action."""
    symbols = {X: "X", O: "O", EMPTY: " "}
    cells = []

    for action, cell in enumerate(game.board):
        if cell != EMPTY:
            label = symbols[cell]
        else:
            label = f"{action}:{action_values[action]:+d}"
            if action == selected_action:
                label += "*"
        cells.append(label.center(7))

    rows = ["|".join(cells[start : start + 3]) for start in range(0, 9, 3)]
    return "\n-------+-------+-------\n".join(rows)


def trace_minimax_game() -> None:
    """Print a complete minimax-versus-minimax game with decision values."""
    game = Board()
    agents = {X: MinimaxAgent(), O: MinimaxAgent()}

    while not game.is_terminal():
        player = "X" if game.current_player == X else "O"
        agent = agents[game.current_player]
        action_values = agent.evaluate_actions(game)
        selected_action = agent.select_action(game)

        print(f"\n{player} to move")
        print(game.render())
        print("\nAction values (+1 win, 0 draw, -1 loss; * selected):")
        print(render_action_values(game, action_values, selected_action))
        print(f"\n{player} chooses square {selected_action}")

        game.apply_action(selected_action)

    print("\nFinal board")
    print(game.render())
    winner = game.winner()
    if winner == EMPTY:
        print("\nResult: draw")
    else:
        winner_name = "X" if winner == X else "O"
        print(f"\nResult: {winner_name} wins")


if __name__ == "__main__":
    trace_minimax_game()

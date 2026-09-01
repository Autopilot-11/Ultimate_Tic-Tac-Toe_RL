from src.g0.game import Board, EMPTY, X

game = Board()

while not game.is_terminal():
    print(game.render())
    player = "X" if game.current_player == X else "O"
    action = int(input(f"{player}, choose a square (0-8): "))
    game.apply_action(action)

print(game.render())
winner = game.winner()
print("Draw!" if winner == EMPTY else f"{'X' if winner == X else 'O'} wins!")
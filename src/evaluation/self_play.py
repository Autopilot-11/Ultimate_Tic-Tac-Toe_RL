"""Self play with random agents"""

from src.agents.random_agent import RandomAgent
from src.g0.game import Board, EMPTY, O, X

def play_game(x_agent, o_agent) -> int:
    game = Board()

    while not game.is_terminal():
        agent = x_agent if game.current_player == X else o_agent
        action = agent.select_action(game)
        game.apply_action(action)
    return game.winner()


def run_random_self_play(num_games: int = 1_000) -> dict[int, int]:
    # x_agent = RandomAgent(seed=0)
    # o_agent = RandomAgent(seed=1)
    # results = {X: 0, O: 0, EMPTY: 0}

    # for _ in range(num_games):
    #     winner = play_game(x_agent, o_agent)
    #     results[winner] += 1

    return run_match(RandomAgent(seed=0),RandomAgent(seed=1),num_games)

def run_match(x_agent, o_agent, num_games: int) -> dict[int, int]:
    results = {X: 0, O: 0, EMPTY: 0}
    for _ in range(num_games):
        winner = play_game(x_agent, o_agent)
        results[winner] += 1
    return results

if __name__ == "__main__":
    results = run_random_self_play()
    print(f"X wins: {results[X]}")
    print(f"O wins: {results[O]}")
    print(f"Draws: {results[EMPTY]}")
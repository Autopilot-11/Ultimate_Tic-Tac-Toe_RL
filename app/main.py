"""FastAPI backend for a single human-versus-random UTTT game."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.agents.random_agent import RandomAgent
from src.g0.game import EMPTY, O, X
from src.g1.game import UBoard

APP_DIRECTORY = Path(__file__).parent
STATIC_DIRECTORY = APP_DIRECTORY / "static"

app = FastAPI(title="Ultimate Tic-Tac-Toe Showcase")
app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY), name="static")

game = UBoard()
random_agent = RandomAgent(seed=0)
last_action: int | None = None


class MoveRequest(BaseModel):
    action: int


def player_name(player: int) -> str | None:
    """Convert an internal player value to a JSON-friendly label."""
    if player == X:
        return "X"
    if player == O:
        return "O"
    return None


def game_state() -> dict:
    """Serialize the current in-memory game for the browser client."""
    winner = game.winner()
    terminal = game.is_terminal()

    if terminal:
        status = "Draw" if winner == EMPTY else f"{player_name(winner)} wins"
    elif game.current_player == X:
        status = "Your turn (X)"
    else:
        status = "Random agent is thinking…"

    return {
        "board": game.board,
        "current_player": player_name(game.current_player),
        "forced_board": game.forced_board,
        "local_winners": [player_name(winner) for winner in game.local_winners],
        "local_complete": game.local_complete,
        "legal_actions": game.legal_actions(),
        "last_action": last_action,
        "terminal": terminal,
        "winner": player_name(winner),
        "status": status,
    }


def reset_game() -> None:
    """Start a new reproducible human-X versus random-O game."""
    global game, random_agent, last_action
    game = UBoard()
    random_agent = RandomAgent(seed=0)
    last_action = None


@app.get("/")
def index() -> FileResponse:
    """Serve the playable browser client."""
    return FileResponse(
        STATIC_DIRECTORY / "index.html", headers={"Cache-Control": "no-store"}
    )


@app.get("/api/game")
def get_game() -> dict:
    """Return the current game state."""
    return game_state()


@app.post("/api/restart")
def restart_game() -> dict:
    """Reset the current game and return the new state."""
    reset_game()
    return game_state()


@app.post("/api/move")
def play_human_move(move: MoveRequest) -> dict:
    """Apply one human move and return the intermediate forced-board state."""
    global last_action
    if game.is_terminal():
        raise HTTPException(status_code=400, detail="The game has already ended.")
    if game.current_player != X:
        raise HTTPException(status_code=400, detail="It is not the human player's turn.")
    if not game.is_legal_move(move.action):
        raise HTTPException(status_code=400, detail="That action is not legal.")

    game.apply_action(move.action)
    last_action = move.action

    return game_state()


@app.post("/api/agent-move")
def play_agent_move() -> dict:
    """Apply the random agent's legal O move after the human turn."""
    global last_action
    if game.is_terminal():
        raise HTTPException(status_code=400, detail="The game has already ended.")
    if game.current_player != O:
        raise HTTPException(status_code=400, detail="It is not the random agent's turn.")

    random_action = random_agent.select_action(game)
    game.apply_action(random_action)
    last_action = random_action

    return game_state()

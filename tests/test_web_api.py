"""Integration tests for the thin playable FastAPI showcase."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_game_returns_an_empty_g1_board():
    client.post("/api/restart")

    response = client.get("/api/game")
    state = response.json()

    assert response.status_code == 200
    assert len(state["board"]) == 81
    assert state["current_player"] == "X"
    assert state["legal_actions"] == list(range(81))


def test_human_move_exposes_the_forced_local_board_before_agent_moves():
    client.post("/api/restart")

    response = client.post("/api/move", json={"action": 38})
    state = response.json()

    assert response.status_code == 200
    assert state["board"][38] == 1
    assert state["current_player"] == "O"
    assert state["forced_board"] == 2
    assert state["legal_actions"] == list(range(18, 27))


def test_agent_move_is_constrained_to_the_forced_local_board():
    client.post("/api/restart")
    client.post("/api/move", json={"action": 38})

    response = client.post("/api/agent-move")
    state = response.json()

    assert response.status_code == 200
    assert state["board"].count(-1) == 1
    assert any(state["board"][action] == -1 for action in range(18, 27))
    assert state["current_player"] == "X"


def test_restart_resets_the_game():
    client.post("/api/move", json={"action": 0})

    response = client.post("/api/restart")
    state = response.json()

    assert response.status_code == 200
    assert state["board"] == [0] * 81
    assert state["forced_board"] is None

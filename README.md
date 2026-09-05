# Recursive Tic-Tac-Toe: Search and Reinforcement Learning

## Research Question
How do search and reinforcement-learning methods scale across a controlled family of recursively nested Tic-Tac-Toe games under fixed compute budgets?

## Game Family
- G0: Tic-Tac-Toe
- G1: Ultimate Tic-Tac-Toe
- G2: Recursive extension (planned)

## Methods
- Random baseline
- Minimax / alpha-beta search
- Monte Carlo Tree Search
- Monte Carlo and temporal-difference learning
- AlphaZero-lite self-play (planned)

## Evaluation
Win/draw/loss, Elo, decision time, simulations per move, and documented failure cases.

## Run the playable G1 demo

Create and activate a virtual environment, then install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the FastAPI server from the project root:

```bash
python -m uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser. You play X; the
server validates your move, applies it to the G1 engine, and then lets the random
agent play O. Use the restart button to begin another game.

Run the test suite with:

```bash
python -m pytest -q
```

## Status
- [x] Stage 0: environment setup and project design
- [x] Stage 1–2: G0 environment, random baseline, and memoized minimax
  - Random self-play (1,000 games; seeds 0 and 1)
  - X wins: 582
  - O wins: 288
  - Draws: 130
- [x] Stage 3–4: G1 environment, random self-play, heuristic, and rollout baselines
- [x] Stage 4A: thin FastAPI showcase for human versus random play

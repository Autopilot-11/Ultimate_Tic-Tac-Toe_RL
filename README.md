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

## Status
- [x] Stage 0: environment setup and project design
- [x] Stage 1: G0 initial environment and random baseline
  - Random self-play (1,000 games; seeds 0 and 1)
  - X wins: 582
  - O wins: 288
  - Draws: 130
- [x] 
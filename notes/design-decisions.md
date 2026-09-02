# Design Decisions

## G0: Ordinary Tic-Tac-Toe foundation

I began with ordinary Tic-Tac-Toe because I wanted to make the game environment
reliable before trying to build agents or reinforcement-learning algorithms.
The board uses `1` for X, `-1` for O, and `0` for an empty square. A game state
contains the board and the player whose turn it is.

The environment owns the rules: it lists legal actions, applies an action,
switches players, checks all eight winning lines, identifies terminal states,
and renders a readable board for debugging. An attempted move after a terminal
state is illegal. I also added `clone()` so search algorithms can test
hypothetical moves without modifying the real game.

## Baseline: random self-play

The first agent was a seeded random agent. It chooses uniformly from the legal
actions, so it is not learning or planning; it gives me a simple baseline and
helps stress-test the environment. In 1,000 seeded random self-play games, X
won 582 times, O won 288 times, and 130 games drew. These are baseline results
for this particular experiment, not universal probabilities, but they show the
expected first-player advantage for X.

## Exact planning: minimax

Minimax is not a learned value function. It is exact adversarial planning for a
deterministic, two-player, zero-sum game. For each possible move, the agent
recursively evaluates future legal states until the game ends. Terminal states
have value `+1` for a win, `0` for a draw, and `-1` for a loss, always from the
perspective of the player whose action is being selected.

At a state where that player moves, minimax chooses the maximum child value. At
a state where the opponent moves, it chooses the minimum child value. There is
no average in minimax because both players are assumed to make optimal choices.
An average would instead describe a random policy. Since G0 has no non-terminal
reward, the recursion only propagates the final terminal outcome backward.

The implementation separates state values from actions. `_minimax_value()`
returns the value of one state, while `evaluate_actions()` scores each legal
action by evaluating its child state. `select_action()` returns the action with
the highest score. The terminal decision trace displays those action scores:
`+1` means a forced win, `0` a forced draw, and `-1` a forced loss under optimal
play.

I added memoization after the basic minimax search worked. The cache stores the
exact solution for `(board, current_player, maximizing_player)`, so repeated
subproblems are not solved again. This makes the implementation top-down dynamic
programming rather than just repeated game-tree search. It is caching exact
answers, not learning from data.

The raw upper bound for a nine-cell board is `3^9 = 19,683` layouts because a
cell can be empty, X, or O. Only 5,478 legal states are reachable when games
stop after a win, including 958 terminal states. Rotations and reflections
reduce these to 765 symmetry-equivalent classes, although G0 is small enough
that symmetry reduction is optional.

## Reuse for G1

G1 should reuse G0's interface and concepts, not force G0's exact `Board`
implementation onto a much more complex game. Both games should expose
`legal_actions()`, `apply_action(action)`, `clone()`, `winner()`,
`is_terminal()`, and `render()`. That lets random agents, evaluators, and later
search code interact with either game in the same way.

G1 will have different internal state: 81 cells, nine local-board outcomes, and
the forced next local board. I will reuse the G0 winning-line definition and
local winner logic where it helps, but write G1's routing and global-win rules
as new code. This keeps the shared API stable while allowing each environment
to represent its own rules cleanly.

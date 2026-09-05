const boardElement = document.getElementById("board");
const statusElement = document.getElementById("status");
const routingElement = document.getElementById("routing");
const restartButton = document.getElementById("restart");

const symbols = { 1: "X", "-1": "O", 0: "" };

function routingText(state) {
  if (state.terminal) {
    return "Game complete. Start a new game to play again.";
  }
  if (state.forced_board === null) {
    return "You may play in any unfinished local board.";
  }
  return `The next move must be in local board ${state.forced_board}.`;
}

function render(state) {
  const legalActions = new Set(state.legal_actions);
  boardElement.replaceChildren();
  statusElement.textContent = state.status;
  routingElement.textContent = routingText(state);

  for (let localBoard = 0; localBoard < 9; localBoard += 1) {
    const localBoardElement = document.createElement("div");
    const isForcedBoard = state.forced_board === localBoard;
    const isComplete = state.local_complete[localBoard];
    localBoardElement.className = "local-board";
    localBoardElement.classList.toggle("forced-board", isForcedBoard);
    localBoardElement.classList.toggle("completed-board", isComplete);
    localBoardElement.setAttribute("aria-label", `Local board ${localBoard}`);

    for (let localCell = 0; localCell < 9; localCell += 1) {
      const action = localBoard * 9 + localCell;
      const value = state.board[action];
      const cell = document.createElement("button");
      const isLegalHumanMove = legalActions.has(action) && state.current_player === "X";
      cell.type = "button";
      cell.className = isLegalHumanMove ? "cell legal" : "cell";
      cell.classList.toggle("last-action", action === state.last_action);
      cell.textContent = symbols[value];
      cell.disabled = !isLegalHumanMove;
      cell.setAttribute("aria-label", `Square ${action}${isLegalHumanMove ? ", legal" : ""}`);

      if (isLegalHumanMove) {
        cell.addEventListener("click", () => playMove(action));
      }
      localBoardElement.appendChild(cell);
    }

    if (isComplete) {
      const result = document.createElement("span");
      result.className = "local-result";
      result.textContent = state.local_winners[localBoard] || "Draw";
      result.setAttribute("aria-label", `${result.textContent} completed local board`);
      localBoardElement.appendChild(result);
    }

    boardElement.appendChild(localBoardElement);
  }
}

async function request(path, options = {}) {
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || "Request failed.");
  }
  return payload;
}

async function loadGame() {
  try {
    render(await request("/api/game"));
  } catch (error) {
    statusElement.textContent = error.message;
  }
}

async function playMove(action) {
  statusElement.textContent = "Applying move…";
  try {
    const state = await request("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action }),
    });
    render(state);
    if (!state.terminal) {
      window.setTimeout(playAgentMove, 500);
    }
  } catch (error) {
    statusElement.textContent = error.message;
  }
}

async function playAgentMove() {
  try {
    render(await request("/api/agent-move", { method: "POST" }));
  } catch (error) {
    statusElement.textContent = error.message;
  }
}

restartButton.addEventListener("click", async () => {
  try {
    render(await request("/api/restart", { method: "POST" }));
  } catch (error) {
    statusElement.textContent = error.message;
  }
});

loadGame();

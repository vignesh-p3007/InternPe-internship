let board = Array(9).fill("");
let currentPlayer = "X";
let gameOver = false;
let mode = "pvp";

let scoreX = 0;
let scoreO = 0;
let scoreDraw = 0;

const cells = document.querySelectorAll(".cell");
const message = document.getElementById("message");
const modeRadios = document.querySelectorAll('input[name="mode"]');
const scoreXEl = document.getElementById("scoreX");
const scoreOEl = document.getElementById("scoreO");
const scoreDrawEl = document.getElementById("scoreDraw");

// Mode selection
modeRadios.forEach(radio => {
    radio.addEventListener("change", () => {
        mode = radio.value;
        restartGame();
    });
});

// Handle cell clicks
cells.forEach(cell => {
    cell.addEventListener("click", () => {
        const index = cell.getAttribute("data-index");
        if (board[index] === "" && !gameOver) {
            makeMove(index, currentPlayer);
            if (mode === "pvc" && !gameOver && currentPlayer === "O") {
                setTimeout(() => computerMove(), 500);
            }
        }
    });
});

// Make a move
function makeMove(index, player) {
    board[index] = player;
    cells[index].textContent = player;
    cells[index].classList.add(player.toLowerCase()); // add "x" or "o"

    if (checkWin(player)) {
        highlightWin(player);
        message.textContent = `Player ${player} wins! 🎉`;
        gameOver = true;
        updateScore(player);
    } else if (board.every(cell => cell !== "")) {
        message.textContent = "It's a draw! 🤝";
        gameOver = true;
        updateScore("draw");
    } else {
        currentPlayer = currentPlayer === "X" ? "O" : "X";
    }
}

// Update scoreboard
function updateScore(winner) {
    if (winner === "X") scoreX++;
    else if (winner === "O") scoreO++;
    else scoreDraw++;

    scoreXEl.textContent = `X: ${scoreX}`;
    scoreOEl.textContent = `O: ${scoreO}`;
    scoreDrawEl.textContent = `Draws: ${scoreDraw}`;
}

// Reset scoreboard
function resetScores() {
    scoreX = 0;
    scoreO = 0;
    scoreDraw = 0;
    scoreXEl.textContent = `X: ${scoreX}`;
    scoreOEl.textContent = `O: ${scoreO}`;
    scoreDrawEl.textContent = `Draws: ${scoreDraw}`;
}

// Check win
function checkWin(player) {
    const winCombos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    return winCombos.some(combo => combo.every(i => board[i] === player));
}

// Highlight winning cells
function highlightWin(player) {
    const winCombos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    winCombos.forEach(combo => {
        if (combo.every(i => board[i] === player)) {
            combo.forEach(i => cells[i].classList.add("win"));
        }
    });
}

// Restart game
function restartGame() {
    board.fill("");
    cells.forEach(cell => {
        cell.textContent = "";
        cell.className = "cell"; // reset classes
    });
    currentPlayer = "X";
    gameOver = false;
    message.textContent = "";
    if (mode === "pvc" && currentPlayer === "O") {
        setTimeout(() => computerMove(), 500);
    }
}

// Smart AI - Minimax
function computerMove() {
    let bestScore = -Infinity;
    let move;
    board.forEach((cell, i) => {
        if (cell === "") {
            board[i] = "O";
            let score = minimax(board, 0, false);
            board[i] = "";
            if (score > bestScore) {
                bestScore = score;
                move = i;
            }
        }
    });
    makeMove(move, "O");
}

// Minimax algorithm
function minimax(boardState, depth, isMaximizing) {
    const scores = { X: -10, O: 10, tie: 0 };
    let result = checkWinnerMinimax(boardState);
    if (result !== null) return scores[result];

    if (isMaximizing) {
        let bestScore = -Infinity;
        boardState.forEach((cell, i) => {
            if (cell === "") {
                boardState[i] = "O";
                let score = minimax(boardState, depth + 1, false);
                boardState[i] = "";
                bestScore = Math.max(score, bestScore);
            }
        });
        return bestScore;
    } else {
        let bestScore = Infinity;
        boardState.forEach((cell, i) => {
            if (cell === "") {
                boardState[i] = "X";
                let score = minimax(boardState, depth + 1, true);
                boardState[i] = "";
                bestScore = Math.min(score, bestScore);
            }
        });
        return bestScore;
    }
}

// Check winner for minimax
function checkWinnerMinimax(b) {
    const winCombos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    for (let combo of winCombos) {
        if (b[combo[0]] && b[combo[0]] === b[combo[1]] && b[combo[1]] === b[combo[2]]) {
            return b[combo[0]];
        }
    }
    if (b.every(cell => cell !== "")) return "tie";
    return null;
}

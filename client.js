// --- Tic-Tac-Toe Client for 15x15 Board ---
// Connects to the new Python server using socket.io

const socket = io('http://localhost:3000');


const boardElement = document.getElementById('board');
const status = document.getElementById('status');
const modeElement = document.getElementById('mode');
const canvas = document.getElementById('win-line-canvas');
const ctx = canvas.getContext('2d');
const BOARD_SIZE = 15;
const PLAYER_X = 'X';
const PLAYER_O = 'O';
let board = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));
let mySymbol = null;
let currentPlayer = PLAYER_X;
const playerName = localStorage.getItem('playerName') || 'Người chơi';
const roomId = localStorage.getItem('roomId') || 'default';

modeElement.textContent = 'PVP';

function createBoard() {
    boardElement.innerHTML = '';
    for (let i = 0; i < BOARD_SIZE; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < BOARD_SIZE; j++) {
            const cell = document.createElement('td');
            cell.dataset.row = i;
            cell.dataset.col = j;
            cell.addEventListener('click', handleCellClick);
            row.appendChild(cell);
        }
        boardElement.appendChild(row);
    }
    const tableRect = boardElement.getBoundingClientRect();
    canvas.width = tableRect.width;
    canvas.height = tableRect.height;
    canvas.style.left = `${tableRect.left}px`;
    canvas.style.top = `${tableRect.top}px`;
}

function handleCellClick(e) {
    if (!mySymbol) {
        status.textContent = 'Chưa được gán ký hiệu!';
        return;
    }
    if (mySymbol !== currentPlayer) {
        status.textContent = 'Chưa đến lượt bạn!';
        return;
    }
    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);
    if (board[row][col]) {
        status.textContent = 'Ô đã được chọn!';
        return;
    }
    socket.emit('make_move', { room_id: roomId, row, col });
}

function updateBoard() {
    const cells = boardElement.getElementsByTagName('td');
    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = 0; j < BOARD_SIZE; j++) {
            const cell = cells[i * BOARD_SIZE + j];
            cell.textContent = board[i][j] || '';
            cell.className = board[i][j] ? board[i][j].toLowerCase() : '';
        }
    }
}

function disableBoard() {
    const cells = boardElement.getElementsByTagName('td');
    for (let cell of cells) {
        cell.removeEventListener('click', handleCellClick);
    }
}

function highlightWinningLine(winInfo) {
    if (!winInfo) return;
    const { direction, start, end } = winInfo;
    const cellWidth = canvas.width / BOARD_SIZE;
    const cellHeight = canvas.height / BOARD_SIZE;
    const startX = start[1] * cellWidth + cellWidth / 2;
    const startY = start[0] * cellHeight + cellHeight / 2;
    const endX = end[1] * cellWidth + cellWidth / 2;
    const endY = end[0] * cellHeight + cellHeight / 2;
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = 'yellow';
    ctx.lineWidth = 5;
    ctx.stroke();
}

function replayGame() {
    socket.emit('replay_game', { room_id: roomId });
}

// --- Socket.IO Event Handlers ---
socket.on('connect', () => {
    status.textContent = 'Đã kết nối đến server!';
    socket.emit('join_room', { room_id: roomId, player_name: playerName });
});

socket.on('connect_error', (err) => {
    status.textContent = 'Không thể kết nối đến server!';
});

socket.on('joined', (data) => {
    mySymbol = data.symbol;
    status.textContent = data.message;
});

socket.on('start_game', (data) => {
    status.textContent = data.message;
    currentPlayer = data.current_player;
});

socket.on('update_board', (data) => {
    board[data.row][data.col] = data.symbol;
    updateBoard();
    currentPlayer = data.current_player;
    status.textContent = data.message;
});

socket.on('game_over', (data) => {
    board[data.row][data.col] = data.symbol;
    updateBoard();
    status.textContent = data.winner ? `${data.winner} (${data.symbol}) thắng!` : data.message;
    if (data.win_info) {
        highlightWinningLine(data.win_info);
    }
    disableBoard();
});

socket.on('opponent_disconnect', () => {
    status.textContent = 'Đối thủ đã ngắt kết nối!';
    disableBoard();
});

socket.on('replay', (data) => {
    mySymbol = data.players[socket.id];
    board = Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null));
    currentPlayer = PLAYER_X;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    createBoard();
    status.textContent = data.message;
});

socket.on('error', (data) => {
    status.textContent = data.message;
});

// --- Initialize Board ---
createBoard();
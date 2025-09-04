import socketio
from aiohttp import web
import asyncio

# Socket.IO server setup
sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

games = {}  # {room_id: {players: {sid: symbol}, board, current_player, roles, player_names}}

# --- Game Logic ---
async def check_winner(board, row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 5):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < 15 and 0 <= c < 15 and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < 15 and 0 <= c < 15 and board[r][c] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

async def is_board_full(board):
    return all(cell is not None for row in board for cell in row)

# --- Socket.IO Events ---
@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    for room_id, game in list(games.items()):
        if sid in game["players"]:
            del game["players"][sid]
            del game["roles"][sid]
            await sio.emit("opponent_disconnect", room=room_id)
            if not game["players"]:
                del games[room_id]

@sio.event
async def join_room(sid, data):
    room_id = data.get("room_id")
    player_name = data.get("player_name", "Player")
    if not room_id:
        await sio.emit("error", {"message": "Missing room_id"}, to=sid)
        return
    await sio.enter_room(sid, room_id)
    if room_id not in games:
        games[room_id] = {
            "players": {sid: "X"},
            "board": [[None] * 15 for _ in range(15)],
            "current_player": "X",
            "roles": {sid: "X"},
            "player_names": {sid: player_name}
        }
        await sio.emit("joined", {"symbol": "X", "message": f"{player_name} (X) chờ đối thủ..."}, to=sid)
    elif len(games[room_id]["players"]) == 1:
        games[room_id]["players"][sid] = "O"
        games[room_id]["roles"][sid] = "O"
        games[room_id]["player_names"][sid] = player_name
        player1_sid = next(s for s in games[room_id]["players"] if s != sid)
        player1_name = games[room_id]["player_names"][player1_sid]
        await sio.emit("joined", {"symbol": "O", "message": f"{player_name} (O) tham gia!"}, to=sid)
        await sio.emit("start_game", {
            "message": f"Bắt đầu! {player1_name} (X) đi trước",
            "current_player": "X"
        }, room=room_id)
    else:
        await sio.emit("error", {"message": "Phòng đã đầy!"}, to=sid)

@sio.event
async def make_move(sid, data):
    room_id = data.get("room_id")
    row = data.get("row")
    col = data.get("col")
    if room_id not in games or sid not in games[room_id]["players"]:
        await sio.emit("error", {"message": "Không tìm thấy phòng hoặc người chơi!"}, to=sid)
        return
    game = games[room_id]
    symbol = game["players"][sid]
    if game["current_player"] != symbol:
        await sio.emit("error", {"message": "Chưa đến lượt bạn!"}, to=sid)
        return
    if not (0 <= row < 15 and 0 <= col < 15) or game["board"][row][col] is not None:
        await sio.emit("error", {"message": "Ô đã được chọn hoặc vị trí không hợp lệ!"}, to=sid)
        return
    game["board"][row][col] = symbol
    player_name = game["player_names"].get(sid, "Người chơi")
    if await check_winner(game["board"], row, col, symbol):
        await sio.emit("game_over", {
            "winner": player_name,
            "symbol": symbol,
            "row": row,
            "col": col
        }, room=room_id)
    elif await is_board_full(game["board"]):
        await sio.emit("game_over", {
            "winner": None,
            "message": "Hòa!",
            "row": row,
            "col": col,
            "symbol": symbol
        }, room=room_id)
    else:
        game["current_player"] = "O" if symbol == "X" else "X"
        opponent_sid = next(s for s in game["players"] if s != sid)
        opponent_name = game["player_names"].get(opponent_sid, "Đối thủ")
        await sio.emit("update_board", {
            "row": row,
            "col": col,
            "symbol": symbol,
            "current_player": game["current_player"],
            "message": f"{opponent_name} ({game['current_player']}) lượt đi"
        }, room=room_id)

@sio.event
async def replay_game(sid, data):
    room_id = data.get("room_id")
    if room_id not in games or sid not in games[room_id]["players"]:
        await sio.emit("error", {"message": "Không tìm thấy phòng hoặc người chơi!"}, to=sid)
        return
    game = games[room_id]
    if len(game["players"]) != 2:
        await sio.emit("error", {"message": "Chờ đối thủ tham gia lại!"}, to=sid)
        return
    for player_sid in game["players"]:
        game["players"][player_sid] = "O" if game["players"][player_sid] == "X" else "X"
        game["roles"][player_sid] = game["players"][player_sid]
    game["board"] = [[None] * 15 for _ in range(15)]
    game["current_player"] = "X"
    x_player = next(s for s, symbol in game["players"].items() if symbol == "X")
    x_player_name = game["player_names"].get(x_player, "Người chơi")
    await sio.emit("replay", {
        "players": game["players"],
        "message": f"Chơi lại! {x_player_name} (X) đi trước"
    }, room=room_id)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=3000) 
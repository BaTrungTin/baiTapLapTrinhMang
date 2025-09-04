# 🎮 Game Caro Online

Một trò chơi Caro (Tic-tac-toe) trực tuyến được phát triển bởi Nhóm 13.

## 📋 Mô tả

Game Caro Online là một trò chơi cờ caro truyền thống được số hóa với giao diện đẹp mắt và trải nghiệm người dùng mượt mà. Người chơi có thể tham gia các trận đấu với bạn bè hoặc thử thách với AI.

## ✨ Tính năng

- 🎯 **Chế độ chơi đa dạng:**
  - Player vs Player (Chơi với bạn bè)
  - Player vs Computer (Thử thách với AI)

- 🎨 **Giao diện đẹp mắt:**
  - Theme màu dark teal hiện đại
  - Animation mượt mà
  - Responsive design

- 🎮 **Trải nghiệm người dùng:**
  - Menu chính với hiệu ứng đẹp
  - Popup hướng dẫn cách chơi
  - Thông tin tác giả

## 🚀 Cách chạy

1. **Cài đặt Python** (phiên bản 3.7 trở lên)

2. **Chạy server:**
   ```bash
   python server.py
   ```

3. **Mở trình duyệt** và truy cập:
   ```
   http://localhost:5000
   ```

## 🎯 Cách chơi

### Luật chơi cơ bản:
- Hai người chơi lần lượt đánh X và O trên bàn cờ
- Mục tiêu: Tạo thành 5 quân cờ liên tiếp (ngang, dọc hoặc chéo)
- Người chơi đầu tiên tạo được 5 quân cờ liên tiếp sẽ thắng
- Nếu bàn cờ đầy mà không ai thắng thì hòa

### Chiến thuật:
- Chặn đường của đối thủ khi họ có 3-4 quân liên tiếp
- Tạo nhiều cơ hội tấn công cùng lúc
- Kiểm soát trung tâm bàn cờ
- Phát triển cả tấn công và phòng thủ

## 📁 Cấu trúc dự án

```
gameCaro/
├── static/
│   ├── css/
│   │   ├── game.css
│   │   ├── mainMenu.css
│   │   └── startGame.css
│   ├── img/
│   │   ├── background.png
│   │   └── ...
│   ├── index.html
│   ├── startGame.html
│   ├── game.html
│   ├── client.js
│   ├── pve.js
│   └── server.py
└── README.md
```

## 🛠️ Công nghệ sử dụng

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python (Flask/Socket.IO)
- **Real-time:** Socket.IO
- **Fonts:** Google Fonts (Bangers, Jersey 15, Jua, Paytone One)

## 👥 Tác giả

**Nhóm 13**
- **Đề tài:** Game Caro Online
- **Môn học:** Lập trình Web

## 📸 Hình ảnh

![Game Interface](static/img/2025-08-07-CARO-GAME-.gif)

## 🔧 Yêu cầu hệ thống

- Python 3.7+
- Trình duyệt web hiện đại (Chrome, Firefox, Safari, Edge)
- Kết nối internet (cho Socket.IO)

## 📝 Ghi chú

- Game sử dụng Socket.IO để giao tiếp real-time giữa các người chơi
- Giao diện được thiết kế responsive, tương thích với mọi thiết bị
- Theme màu dark teal tạo cảm giác hiện đại và dễ chịu cho mắt

## 🎉 Cảm ơn

Cảm ơn bạn đã sử dụng Game Caro Online! Chúc bạn chơi game vui vẻ! 🎮

# Week 2 Task – Tic Tac Toe Game 🎮

## 📌 Objective
Develop an interactive **Tic Tac Toe game** using **HTML, CSS, and JavaScript** with the option to play in two modes:  
- **Player vs Player (PvP)**  
- **Player vs Computer (PvC)**  

The computer player should use the **Minimax algorithm** to make optimal moves.

---

## 🛠️ Features
- 🎨 **Visually appealing UI** with responsive design.  
- 🧑‍🤝‍🧑 **Player vs Player mode** – two players alternate turns.  
- 🤖 **Player vs Computer mode** – Computer AI powered by **Minimax**.  
- 🏆 **Scoreboard tracking** for:
  - Wins of `X`
  - Wins of `O`
  - Draw matches
- 🔄 **Restart game option** – resets only the board.  
- ♻️ **Reset scoreboard option** – clears scores back to zero.  
- ✨ Different colors for `X` (red) and `O` (blue).  
- 🎉 Winning cells are highlighted.  

---

## ⚙️ Tech Stack
- **HTML** – Game board and layout.  
- **CSS** – Styling for board, scoreboard, and animations.  
- **JavaScript** – Game logic, scoreboard, and Minimax AI.  
- **Flask (optional)** – To serve the game with `app.py`.  

---

## 📂 Project Structure

Week2_TicTacToe/    
├── solution/   
│ ├── static/   
│ │ ├── script.js # Game logic (PvP + AI + styling) 
│ │ └── style.css # Styling 
│ ├── templates/    
│ │ └── index.html # Game UI    
│ └── app.py # Flask backend (optional) 
├── Task_Description.md # Task overview 
└── Notes.md # Developer notes  

---

## 🚀 How to Run
1. Clone this repository or download the project files.  
2. Open `index.html` directly in your browser to play.  
3. (Optional) If using Flask:  
   ```bash
   python app.py
   ```

Then visit http://127.0.0.1:5000/ in your browser.

---

## 👨‍💻 Author
**Vignesh Poojari**  
[LinkedIn](https://www.linkedin.com/in/vignesh-p3007)  

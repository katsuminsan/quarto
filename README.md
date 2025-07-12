# Quarto Game (Python)

This repository contains a web-based implementation of the **Quarto** board game using Python and Flask's DEMO.

Quarto is a two-player strategy game where players take turns choosing and placing pieces on a 4x4 board. The goal is to line up four pieces that share a common attribute.

Please check the official website here.
https://en.gigamic.com/modern-classics/1049-quarto-3421271300410.html

## 🧩 Features

- Complete logic for the Quarto game  
- Turn-based play between human and computer (`Opponent.py`)  
- Web interface using Flask and HTML templates  
- Modular Python design with game logic (`quarto.py`), item definitions (`items.py`), and AI opponent  

## 📁 Project Structure

```
quarto-main/
├── app.py            # Flask app entry point
├── quarto.py         # Core game logic (board, winning conditions)
├── items.py          # Piece definitions and attributes
├── Opponent.py       # AI logic or computer opponent behavior
├── static/           # (Optional) CSS/JS or image files
└── views/
    ├── base.html     # Base HTML layout (likely includes header/footer)
    └── bord.html     # Game board display page
```

## 🚀 How to Run

### Prerequisites

- Python 3.x  
- Flask  

### Install dependencies

```bash
pip install flask
```

### Run the application

```bash
python app.py
```

Then open your browser and visit:  
📍 [http://localhost:5000](http://localhost:5000)

## 📸 Screenshots

_Add screenshots of the game board or interface if available._

## 🤖 About the AI

The opponent logic is implemented in `Opponent.py`, and may include simple rules or heuristics to simulate a challenging gameplay experience.

## 📜 License
This project is currently not licensed.

## ✍️ Author

Maintained by [katsuminsan](https://github.com/katsuminsan)  
Feel free to open issues or pull requests!


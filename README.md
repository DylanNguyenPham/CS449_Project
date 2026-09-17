# CS449_Project
Your customer asks you to develop the software that allows to play the Peg Solitaire BrainVita game

# Peg Solitaire - CS 449

A Python-based implementation of the classic English Peg Solitaire game featuring a custom graphical user interface and interactive customization options.

---

## 🛠️ Project Decisions & Technical Stack

* **Programming Language:** **Python 3.x** — Chosen for its readability, rapid prototyping capabilities, and rich ecosystem of game development and testing libraries.
* **GUI Library:** **Pygame** — Utilized for 2D graphics rendering, event handling (mouse clicks, window states), and smooth 60 FPS game loop execution.
* **IDE:** **Visual Studio Code (VS Code)** — Used for writing code, managing files across a modular structure (`Peg_Solitaire.py`, `Gui.py`, `Classes.py`), and running terminal commands.
* **Unit Testing Framework:** **`unittest`** — Python's built-in testing framework used to verify core game logic, board dimensions, starting states, and peg counts with detailed verbosity.
* **Programming Style:** **Modular Object-Oriented & Procedural Programming** — Code is separated into distinct modules (`Classes.py` for reusable UI components like buttons, `Gui.py` for board rendering and state management, and `Peg_Solitaire.py` as the main entry point).
* **Project Hosting Site:** **GitHub** — Used for version control, issue tracking, and collaborative project sharing.

---

## 📁 Project Structure

```text
├── Peg_Solitaire.py   # Main entry point and game loop
├── Gui.py             # Board rendering, UI elements, and color states
├── Classes.py         # Reusable UI components (Button class)
└── test_board.py      # Unit tests for board configuration and logic

# chesspsr
Chess paper scissors rock strategy game

This Python script implements a graphical version of the Rock Paper Scissors board game using Tkinter. It's a two-player game where each player tries to capture the other's pieces by moving their own pieces across an 8x8 grid. The game incorporates the classic rock-paper-scissors mechanics for battles between pieces.

# Features
Graphical User Interface: Utilizes Tkinter for a user-friendly graphical interface.
Piece Movement: Players can move their pieces around the board with the goal of capturing the opponent's pieces or reaching the opponent's home square.
Battles: When pieces occupy the same square, a battle occurs, decided by rock-paper-scissors rules.
Visibility Mechanics: Pieces can be hidden or revealed based on game actions, adding a layer of strategy.
Winning Conditions: The game ends when a player's piece reaches the opponent's home square.
# Requirements
To run this script, you need Python installed on your machine along with the following packages:

Tkinter (usually comes with Python)
PIL (Python Imaging Library) for image handling
You can install PIL using pip:

bash
Copy code
pip install Pillow
How to Run
To start the game, execute the script from your terminal or command prompt:

bash
Copy code
python rock_paper_scissors_game.py
Make sure you're in the correct directory where the script is located.

Gameplay Instructions
Start the Game: Upon launching, players will be prompted to place their starting pieces (Rock, Paper, Scissors) on specific squares adjacent to their home square.
Take Turns: Players take turns moving their pieces across the board. Each turn, a player can either:
Move a Piece: Select one of your pieces and move it to an adjacent square.
Spawn a New Piece: If your home square is not occupied, you can spawn a new piece there.
Engage in Battles: If you move your piece to a square occupied by an opponent's piece, a battle occurs. The outcome is based on the classic rock-paper-scissors rules:
Rock defeats Scissors.
Scissors defeat Paper.
Paper defeats Rock.
Win the Game: The first player to move a piece to the opponent's home square wins the game.
Customizing the Game
Changing Icons
You can customize the icons used for each piece by replacing the image files in the images directory. Ensure the new images are named accordingly (e.g., P1rock.png, P2scissors.png).

# Adjusting Board Size
While the default board size is 8x8, you can adjust it by modifying the board and buttons matrix dimensions in the GameGUI class initialization.

# Contributing
Feel free to fork the repository and submit pull requests to contribute to the game's development. Whether it's adding new features, improving the UI, or fixing bugs, your contributions are welcome.

License
This project is open-source and available under the MIT License.

Enjoy playing Rock Paper Scissors Board Game!

# To Do:

* Change setup_ai_game function to invoke more detailed dialog with additional configuration options
  * Add option to randomise initial piece types to expedite setup
* Handle end game properly, offering restart or close application
* Update AI with better logic, make decisions based on opportunities and moves remaining:
  * aim to win if possible
  * aim to avoid losing next turn if possible
  * aim to capture pieces if possible this turn
  * else carry out existing logic to move piece towards enemy home

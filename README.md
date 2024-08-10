# chesspsr
Chess paper scissors rock strategy game

This Python script implements a graphical version of the Rock Paper Scissors board game using Tkinter. It's a two-player game where each player tries to capture the other's pieces by moving their own pieces across an 8x8 grid. The game incorporates the classic rock-paper-scissors mechanics for battles between pieces.

The end objective is to build this into an environment where an AI agent can be trained with RL to play the game and develop effective strategies. It is possible that the rules will need to be chanegd to accomodate a dynamic and rich playing experience, and the use of AI is ultimately intended to refine the ruleset.

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
Changing Icons:
You can customize the icons used for each piece by replacing the image files in the images directory. Ensure the new images are named accordingly (e.g., P1rock.png, P2scissors.png).

# Adjusting Board Size
While the default board size is 8x8, you can adjust it by modifying the board and buttons matrix dimensions in the GameGUI class initialization.

# Contributing
Feel free to fork the repository and submit pull requests to contribute to the game's development. Whether it's adding new features, improving the UI, or fixing bugs, your contributions are welcome.

License
This project is open-source and available under the MIT License.

Enjoy playing Rock Paper Scissors Board Game!

# new mechanics to consider:

## Respec
if the current mechanics end in perpetual stalemate, consider a 'respec' action where a player can make a revealed piece they own hidden again, and optionally change the type 

# To Do:

* Change setup_ai_game function to invoke more detailed dialog with additional configuration options
  * Add option to choose different AI agents
* Update AI with better logic, make decisions based on opportunities and moves remaining:
  * aim to avoid losing next turn if possible
    * DONE will move a piece to a defensive square if possible
    * MUST check that a move wont open a new pathway for the threat to attack. This should enable other pieces to occupy other squares that are in the attackers pathway
  * aim to capture pieces if possible this turn
  * else carry out existing logic to move piece towards enemy home
  * 


 Updated with ruleset used to prompt Claude:

Create an interface and engine for a simple game that is played on a chess board between two players. the corner A1 is the home square of player 1 (white), and corner H8 is the home square of player 2 (black). Each player controls their pieces, and if a player manages to get a piece to the opponent's home square, then they win. The pieces have identities that are decided when they are placed. The identities are: red, green and blue. The identities are known to the player that controls them, but are initially hidden from the opponent. At the beginning of the game, each player starts with a piece on each adjacent square to their home square.  Players take turns by taking actions. Actions consume action points, and at the beginning of each player's turn they have three action points. A player may move a piece across an edge to the next square (up or across, but not diagonally), and each move action consumes 1 action point. A piece may not be moved on to a square that is already occupied by a player's own piece. If a player attempts to move a piece to a square occupied by an opponent's piece, this is an 'attack'. When a piece attacks another piece, both pieces hidden identities are permanently revealed, and the winner is based on the following: red defeats green, green defeats blue, and blue defeats red. The winner of the attack occupies the attacked square and the losing piece is removed from the board. If both pieces have the same identify, then the attack is a draw, and both pieces remain on their original squares. A player may 'redeploy' a piece for 2 action points. When a piece is redeployed, it remains in its current location, but its identity is hidden from the opponent if it was previously revealed, and the controlling player may choose a new identity for that piece. A player may 'respawn' a piece on their home square for 3 points if the following conditions are met: that no other piece is currently on their home square, and that they control fewer than three other pieces on the board.

Create this game in javascript. Make the interface work as such: to move, a player clicks on the piece they want to move, then clicks on the square they want to move to. Ensure that only the legal squares that a player may move to are highlighted as options. To redeploy, after selecting a piece, instead of clicking on a square to move to, the player may click on a button that allows them to redeploy. After clicking on the button, they may click on one of three buttons to choose the new identify of the piece was selected. Ensure this option is only available if the player has more than 1 action point available. To respawn, a player clicks on their home square, then is presented with the same three buttons to choose the new piece's identify as with the redeploy button. After selecting the identity, the new piece appears in the home square. Ensure this option is only available if a player has 3 action points (this is the only action they may take in their turn if they choose this, since it consumes all 3 points). Once a player consumes all three of their action points in their turn, it switches to the opponents turn.

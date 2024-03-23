import tkinter as tk
from tkinter import Toplevel, Button
from tkinter import messagebox
from PIL import Image, ImageTk

class Piece:
    def __init__(self, piece_type, player, is_revealed=False):
        self.piece_type = piece_type  # "Paper", "Scissors", or "Rock"
        self.player = player # Player 1 or Player 2
        self.is_revealed = is_revealed

class Player:
    def __init__(self, home_square):
        self.home_square = home_square
        self.pieces = []  # This will hold Piece objects

class ChoosePieceTypeDialog(Toplevel):
    def __init__(self, parent, title="Choose Piece Type"):
        super().__init__(parent)
        self.geometry("200x150")
        self.title(title)
        self.result = None
        
        options = ["Rock", "Paper", "Scissors"]
        for option in options:
            btn = Button(self, text=option, command=lambda o=option: self.set_choice_and_destroy(o))
            btn.pack(pady=10)
        
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        parent.wait_window(self)

    def set_choice_and_destroy(self, choice):
        self.result = choice
        self.destroy()

    def on_close(self):
        self.result = None
        self.destroy()

class PieceTypeDialog(Toplevel):
    def __init__(self, parent, title, message, options):
        super().__init__(parent)
        self.geometry("300x100")

        tk.Label(self, text=message).pack(pady=(10, 0))

        self.result = None  # Prepare to store the result temporarily

        def set_choice_and_destroy(choice):
            self.result = choice  # Store the result
            self.destroy()

        for option in options:
            Button(self, text=option, command=lambda o=option: set_choice_and_destroy(o)).pack(side="left", expand=True, padx=5, pady=10)

        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle the window close button
        parent.wait_window(self)  # Wait here until the dialog closes

    def on_close(self):
        """Handle the dialog being closed via the window manager."""
        self.result = None  # No selection was made
        self.destroy()

class GameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Rock Paper Scissors Board Game")
        
        self.board = [[None for _ in range(8)] for _ in range(8)]  # Placeholder for game board data
        self.buttons = [[None for _ in range(8)] for _ in range(8)]  # Buttons for the GUI
        
        self.current_turn = 0  # Start with player 1
        self.selected_piece = None  # Track selected piece for moving

        # Desired icon size (width, height)
        self.icon_size = (64, 64)  # Adjust based on your button size
        
        self.load_icons()

        # Add a status label to display whose turn it is
        self.status_label = tk.Label(self.master, text="Player 1's turn", font=('Helvetica', 16))
        self.status_label.grid(row=8, column=0, columnspan=8)  # Adjust grid parameters as needed

        self.move_count = 0  # Track the number of moves made in the current turn
        self.home_squares = {1: (7, 0), 2: (0, 7)}  # Assuming Player 1's home is at (7, 0) and Player 2's at (0, 7)

        self.create_board()
        self.initialize_game()
        self.announce_turn()
    
    def load_icons(self):
        icon_paths = {
            'rock_player1': 'images/P1rock.png',
            'scissors_player1': 'images/P1scissors.png',
            'paper_player1': 'images/P1paper.png',
            'rock_player2': 'images/P2rock.png',
            'scissors_player2': 'images/P2scissors.png',
            'paper_player2': 'images/P2paper.png',
            'hidden_player1': 'images/P1hidden.png',
            'hidden_player2': 'images/P2hidden.png',
        }
        
        self.icons = {}
        for key, path in icon_paths.items():
            image = Image.open(path)
            # Resize the image to fit the button, optionally maintaining aspect ratio
            # Use Image.Resampling.LANCZOS (formerly Image.ANTIALIAS) for better quality
            image = image.resize(self.icon_size, Image.Resampling.LANCZOS)
            self.icons[key] = ImageTk.PhotoImage(image)

    def announce_turn(self):
        # Announce the beginning of a player's turn
        player = self.current_turn + 1
        messagebox.showinfo("Turn", f"Player {player}'s turn")
        self.update_turn_status()

    def update_turn_status(self):
        # Update the status label with the current player's turn
        player = self.current_turn + 1
        self.status_label.config(text=f"Player {player}'s turn")

    def create_board(self):
        for row in range(8):
            for col in range(8):
                btn = tk.Button(self.master, text=' ', width=8, height=4, command=lambda r=row, c=col: self.on_square_clicked(r, c),
                                borderwidth=3, activebackground='blue')  # Highlight border set to 2px, default color white
                btn.grid(row=row, column=col, sticky='nsew')
                self.buttons[row][col] = btn

        # Configure the grid to allow cell resizing
        for i in range(8):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def on_square_clicked(self, row, col):
        print(f"Clicked: {row}, {col}, Selected: {self.selected_piece}, Move Count: {self.move_count}")  # Debug print

        # Check if there's a piece on the clicked square and print details
        piece = self.board[row][col]
        if piece:
            print(f"Piece present: Yes, Type: {piece.piece_type}, Owner: Player {piece.player}")
        else:
            print("Piece present: No")
        
        # Home square logic
        if (row, col) == self.home_squares[self.current_turn + 1] and not self.board[row][col] and self.move_count == 0:
            self.spawn_piece(self.current_turn + 1, row, col)
            self.switch_turn()  # Switch turn after spawning
        elif self.selected_piece:
            # Attempt to move selected piece to the clicked square
            if self.is_valid_move(self.selected_piece, (row, col)):
                self.move_piece(self.selected_piece, (row, col))
                self.move_count += 1
                print(f"Move made to: {row}, {col}. Move Count: {self.move_count}")
                if self.move_count == 3:  # After making three moves, switch turns
                    self.switch_turn()
                self.selected_piece = None  # Reset selected_piece after a successful move
            else:
                print("Invalid move. Try again.")
                self.selected_piece = None  # Consider resetting selected_piece if the move is invalid
        else:
            # Select a piece to move if within move limit
            if self.move_count < 3 and self.is_valid_selection(row, col):
                self.selected_piece = (row, col)
                print(f"Piece at {row}, {col} selected. Move Count: {self.move_count}")
            else:
                print("Move limit reached or invalid selection.")

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn
        self.move_count = 0  # Reset move count for the new turn
        self.selected_piece = None  # Ensure selected_piece is reset when switching turns
        self.announce_turn()
        self.update_board()  # Update board to reflect any changes
    
    def initialize_game(self):
        # Define the starting positions for Player 1 and Player 2
        player1_positions = [("A2", (6, 0)), ("B2", (6, 1)), ("B1", (7, 1))]
        player2_positions = [("G8", (0, 6)), ("G7", (1, 6)), ("H7", (1, 7))]
        
        # Loop through each player's positions to initialize pieces
        for player_id, positions in enumerate([player1_positions, player2_positions], start=1):
            self.prompt_for_initial_pieces(player_id, positions)
            
        self.update_board()

    def prompt_for_initial_pieces(self, player_id, positions):
        piece_types = ["Rock", "Paper", "Scissors"]
        for square, (row, col) in positions:
            message = f"Player {player_id}, select a type for {square}"
            dialog = PieceTypeDialog(self.master, "Piece Selection", message, piece_types)
            
            choice = dialog.result  # Access the result directly after the dialog has been handled
            
            if choice:  # If a choice was made
                piece = Piece(choice, player_id, is_revealed=False)  # Assuming pieces are initially revealed
                self.board[row][col] = piece
                # Use icons instead of text for pieces
                icon_key = f"{choice.lower()}_player{player_id}"
                self.buttons[row][col].config(image=self.icons[icon_key], bg="white")
                # Store a reference to prevent garbage collection
                self.buttons[row][col].image = self.icons[icon_key]
                piece_types.remove(choice)

    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        from_piece = self.board[from_row][from_col]
        to_piece = self.board[to_row][to_col]

        if from_piece and self.is_valid_move(from_pos, to_pos):
            # Check if we're attempting to move onto an opponent's piece (initiating a battle)
            if to_piece and to_piece.player != from_piece.player:
                # Set both pieces to be revealed
                from_piece.is_revealed = True
                if to_piece:  # Check to ensure there's a defending piece
                    to_piece.is_revealed = True
                
                # Resolve the battle based on your game's rules
                outcome = self.resolve_battle(from_piece, to_piece)
                if outcome == "win":
                    # Attacker wins, replace the defender's piece with the attacker's
                    self.board[to_row][to_col] = from_piece
                    self.board[from_row][from_col] = None
                    print(f"Player {from_piece.player}'s {from_piece.piece_type} wins the battle.")
                elif outcome == "draw":
                    # If the battle is a draw, no pieces are moved or removed
                    self.update_board()
                    print("The battle ends in a draw. No pieces are moved.")
                    return  # Early return to skip the win condition check and board update
                else:  # outcome == "lose"
                    # Attacker loses, remove the attacker's piece from the board
                    self.board[from_row][from_col] = None
                    print(f"Player {from_piece.player}'s {from_piece.piece_type} loses the battle.")
            else:
                # Move the piece to the new position if not initiating a battle
                self.board[to_row][to_col] = from_piece
                self.board[from_row][from_col] = None
                print(f"Moved {from_piece.piece_type} from {from_pos} to {to_pos}")

            # Check for win condition after the move or battle
            if self.check_win_condition():
                tk.messagebox.showinfo("Game Over", f"Player {self.current_turn + 1} wins!")

            # Update the board to reflect the new state
            self.update_board()
        else:
            print("Invalid move.")

    def resolve_battle(self, attacker, defender):
        # Define wins-against relationships
        wins_against = {"Rock": "Scissors", "Scissors": "Paper", "Paper": "Rock"}

        if wins_against[attacker.piece_type] == defender.piece_type:
            return "win"
        elif attacker.piece_type == defender.piece_type:
            return "draw"
        else:
            return "lose"

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Ensure move is within board boundaries
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            print("Outside boundaries")
            return False
        
        # Ensure move is to an adjacent square (modify as needed for your game's rules)
        if abs(from_row - to_row) > 1 or abs(from_col - to_col) > 1:
            print("Must move to an adjacent square.")
            return False
        
        # Ensure starting and ending positions are not the same
        if from_pos == to_pos:
            print("Must move to a different square")
            return False
        
        from_piece = self.board[from_row][from_col]
        to_piece = self.board[to_row][to_col]
        
        # Ensure there is a piece at the starting position
        if not from_piece:
            return False
        
        # Ensure the move is made by the current player's piece
        if from_piece.player != self.current_turn + 1:
            print(f"This move is not allowed for Player {self.current_turn + 1}.")
            return False
        
        # Check if the target square is occupied by the player's own piece
        if to_piece and to_piece.player == from_piece.player:
            print("Cannot move onto your own piece.")
            return False

            # Check if the target square is occupied by the opponent's piece for a possible battle
        if to_piece and to_piece.player != from_piece.player:
        # Check for invalid battle condition: both pieces are revealed and of the same type
            if from_piece.is_revealed and to_piece.is_revealed and from_piece.piece_type == to_piece.piece_type:
                print("Cannot attack: both pieces are revealed and of the same type.")
                return False
            else:
                return True  # Valid move for initiating a battle

        # Check other move validity conditions specific to your game's rules...

        return True  # Assuming other conditions are met

    def spawn_piece(self, player, row, col):
        piece_type = self.choose_piece_type()
        if piece_type:
            new_piece = Piece(piece_type, player, is_revealed=False)
            self.board[row][col] = new_piece
            # Update the board visualization as necessary
            self.update_board()
            print(f"Spawned {piece_type} for Player {player}")
        else:
            print("Piece spawning cancelled.")

    def choose_piece_type(self):
        dialog = ChoosePieceTypeDialog(self.master, "Choose Piece Type")
        return dialog.result

    def can_capture(self, attacker, defender):
        """Determine if the attacking piece can capture the defending piece."""
        # Simplified example of capture logic based on piece types
        # Assuming attacker and defender are strings like 'R', 'P', 'S' for rock, paper, scissors
        rules = {'R': 'S', 'P': 'R', 'S': 'P'}
        attacker = attacker.upper()
        defender = defender.upper()
        return rules.get(attacker) == defender

    def is_valid_selection(self, row, col):
        selected_piece = self.board[row][col]
        
        # Ensure there is a piece at the selected position
        if not selected_piece:
            print("No piece at the selected position.")
            return False

        # Check if the selected piece belongs to the current player
        # Note: Adjusted to use the `player` attribute of the Piece instance
        if selected_piece.player != self.current_turn + 1:
            print(f"This piece does not belong to Player {self.current_turn + 1}.")
            return False

        # The selection is valid
        return True

    def check_win_condition(self):
        # Check Player 1's victory condition: Player 1 piece is at Player 2's home square
        if self.board[0][7] is not None and self.board[0][7].player == 1:
            print("Player 1 wins!")
            return True
        # Check Player 2's victory condition: Player 2 piece is at Player 1's home square
        if self.board[7][0] is not None and self.board[7][0].player == 2:
            print("Player 2 wins!")
            return True
        return False

    def update_board(self):
        print(f"current turn: {self.current_turn + 1}")
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:  # If there's a piece in this square
                    # Determine the base key for the icon dictionary based on piece attributes
                    if piece.is_revealed or piece.player == self.current_turn + 1:
                        icon_key = f"{piece.piece_type.lower()}_player{piece.player}"
                    else:
                        # For a hidden piece from the opponent's perspective
                        icon_key = f"hidden_player{piece.player}"

                    self.buttons[row][col].config(image=self.icons[icon_key])

                    # For the current player's hidden pieces, set a grey background; otherwise, white
                    if piece.player == self.current_turn + 1 and not piece.is_revealed:
                        self.buttons[row][col].config(bg="grey")
                    else:
                        self.buttons[row][col].config(bg="white")
                else:  # No piece in this square, reset the button
                    self.buttons[row][col].config(image='', bg="white")

                # Ensure a reference to the image is kept to prevent it from being garbage collected
                if piece:
                    self.buttons[row][col].image = self.icons.get(icon_key, '')

def main():
    root = tk.Tk()
    game_gui = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


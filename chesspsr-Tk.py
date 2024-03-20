import tkinter as tk
from tkinter import simpledialog
from tkinter import Toplevel, Button
from tkinter import messagebox
from tkinter import PhotoImage
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
                btn = tk.Button(self.master, text=' ', width=8, height=4, command=lambda r=row, c=col: self.on_square_clicked(r, c))
                btn.grid(row=row, column=col, sticky='nsew')
                self.buttons[row][col] = btn

        # Configure the grid to allow cell resizing
        for i in range(8):
            self.master.grid_rowconfigure(i, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def on_square_clicked(self, row, col):
        if self.selected_piece:
            # Attempt to move selected piece to the clicked square
            if self.is_valid_move(self.selected_piece, (row, col)):
                self.move_piece(self.selected_piece, (row, col))
                self.switch_turn()  # Switch turns after a valid move
            else:
                print("Invalid move. Try again.")
            self.selected_piece = None  # Reset selection regardless of move validity
        else:
            # Select a piece to move
            if self.is_valid_selection(row, col):
                self.selected_piece = (row, col)
                print(f"Piece at {row}, {col} selected. Now select where to move it.")
            else:
                print("Invalid selection. Select one of your pieces.")

        self.update_board()

    def switch_turn(self):
        # Switch the current turn to the other player
        self.current_turn = 1 - self.current_turn
        self.announce_turn()  # Announce the next player's turn

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
                piece = Piece(choice, player_id, is_revealed=False)
                self.board[row][col] = piece
                btn_text = choice[0].capitalize()  # Showing the initial letter
                self.buttons[row][col].config(text=btn_text)
                piece_types.remove(choice)

    def move_piece(self, from_pos, to_pos):
        # Extract row and column from positions
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # Example logic to check if the move is valid and perform it
        piece = self.board[from_row][from_col]
        if piece and self.is_valid_move(from_pos, to_pos):
            self.board[to_row][to_col] = self.board[from_row][from_col]
            self.board[from_row][from_col] = None
            print(f"Moved {piece} from {from_pos} to {to_pos}")
            self.current_turn = 1 - self.current_turn  # Switch turns
        else:
            print("Invalid move.")

        if self.check_win_condition():
            tk.messagebox.showinfo("Game Over", f"Player {self.current_turn + 1} wins!")
        self.update_board()

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
        
        # Check other move validity conditions specific to your game's rules...

        return True  # Assuming other conditions are met

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
        # Directly check the opponent's home square for the presence of a piece
        if self.board[7][0] is not None and self.board[7][0] in self.players[1].pieces:
            print("Player 1 wins!")
            return True
        if self.board[0][7] is not None and self.board[0][7] in self.players[0].pieces:
            print("Player 2 wins!")
            return True
        return False

    def update_board(self):
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


class Piece:
    def __init__(self, piece_type, is_revealed=False):
        self.piece_type = piece_type  # "Paper", "Scissors", or "Rock"
        self.is_revealed = is_revealed

class Player:
    def __init__(self, home_square):
        self.home_square = home_square
        self.pieces = []  # This will hold Piece objects

class Game:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # 8x8 grid
        self.players = [Player("A1"), Player("H8")]
        self.current_turn = 0  # Player 1 starts

    def initial_board_setup(self):
        # Define the squares adjacent to each player's home square
        player1_squares = [("A2", (6, 0)), ("B2", (6, 1)), ("B1", (7, 1))]
        player2_squares = [("G8", (0, 6)), ("G7", (1, 6)), ("H7", (1, 7))]
        
        # Iterate through both players for initial setup
        for player_id, squares in enumerate([player1_squares, player2_squares]):
            print(f"\nPlayer {player_id + 1}, place your initial pieces.")
            types_remaining = ["Rock", "Paper", "Scissors"]
            
            for square_name, (row, col) in squares:
                piece_type = self.prompt_for_piece_type(square_name, types_remaining)
                # Remove the selected type from remaining types
                types_remaining.remove(piece_type)
                # Spawn the piece on the board (initially hidden)
                new_piece = Piece(piece_type, is_revealed=False)
                self.players[player_id].pieces.append(new_piece)
                self.board[row][col] = new_piece

    def prompt_for_piece_type(self, square_name, types_remaining):
        print(f"Select a type from {types_remaining} to occupy {square_name}")
        while True:
            piece_type = input("> ").capitalize()
            if piece_type in types_remaining:
                return piece_type
            else:
                print(f"Invalid type. Please select from {types_remaining}.")

    def display_board(self):
        player_turn = self.current_turn % 2  # Determines which player's turn it is
        piece_symbols = {
            "Rock": "R",
            "Paper": "P",
            "Scissors": "S"
        }

        for row in self.board:
            row_display = []
            for piece in row:
                symbol = " "
                if piece:
                    # Determine if the piece belongs to the current player or the opponent
                    is_current_player_piece = piece in self.players[player_turn].pieces

                    # Determine symbol based on piece type and visibility
                    if is_current_player_piece or piece.is_revealed:
                        symbol = piece_symbols[piece.piece_type] if piece in self.players[0].pieces else piece_symbols[piece.piece_type].lower()
                    else:
                        symbol = "H" if piece in self.players[0].pieces else "h"
                    
                    # Append 'H' or 'h' to hidden pieces
                    if not piece.is_revealed:
                        symbol += "H" if piece in self.players[0].pieces else "h"

                row_display.append(symbol)

            print(' | '.join(row_display))
            print('-' * 71)  # Print a divider between rows for readability
                   
    def spawn_piece(self, player_id, piece_type):
        # Retrieve the home square coordinates for the player
        home_square = self.players[player_id].home_square
        # Convert the alphanumeric home square to row and column indices
        row = 8 - int(home_square[1])  # Convert numeric part to row index
        col = ord(home_square[0].upper()) - ord('A')  # Convert letter to column index
        
        # Check if a piece can be spawned (player has fewer than three pieces)
        if len(self.players[player_id].pieces) < 3:
            new_piece = Piece(piece_type)
            self.players[player_id].pieces.append(new_piece)
            self.board[row][col] = new_piece
        else:
            print("Cannot spawn piece, maximum pieces on board reached.")

    def move_piece(self, player_id, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position
        piece = self.board[from_row][from_col]

        # Initial checks for validity of the move
        if not (piece and
                0 <= to_row < 8 and 0 <= to_col < 8 and
                abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1 and
                (from_row != to_row or from_col != to_col)):  # Ensure it's not the same square
            return False  # Move is invalid
        
        # Check if the target square is empty or occupied by opponent
        if self.board[to_row][to_col] is None or self.board[to_row][to_col] not in self.players[player_id].pieces:
            if self.board[to_row][to_col] is not None:
                # Battle happens here, if necessary you can adjust battle logic to return specific outcomes
                self.check_for_battle(player_id, from_position, to_position)
            # Execute the move
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            return True
        else:
            # Move is invalid because the target is occupied by player's own piece
            return False
        
    def check_for_battle(self, player_id, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position
        attacker = self.board[from_row][from_col]
        defender = self.board[to_row][to_col]

        # Assuming both pieces are revealed for the battle
        attacker.is_revealed = True
        defender.is_revealed = True

        outcome = {"Paper": "Rock", "Rock": "Scissors", "Scissors": "Paper"}
        if outcome[attacker.piece_type] == defender.piece_type:
            # Attacker wins
            self.board[to_row][to_col] = attacker
            self.board[from_row][from_col] = None
            self.players[1 - player_id].pieces.remove(defender)  # Remove defender
        elif attacker.piece_type != defender.piece_type:
            # Defender wins, attacker is removed
            self.board[from_row][from_col] = None
            self.players[player_id].pieces.remove(attacker)  # Remove attacker

    def check_win_condition(self):
        # Directly check the opponent's home square for the presence of a piece
        if self.board[7][0] is not None and self.board[7][0] in self.players[1].pieces:
            print("Player 1 wins!")
            return True
        if self.board[0][7] is not None and self.board[0][7] in self.players[0].pieces:
            print("Player 2 wins!")
            return True
        return False

def is_valid_position(pos):
    if len(pos) != 2:
        return False
    col, row = pos[0].upper(), pos[1]
    return col in "ABCDEFGH" and row.isdigit() and 1 <= int(row) <= 8

def run_game_console():
    game = Game()
    # Execute the initial setup routine before the game starts
    game.initial_board_setup()
    game.display_board()

    while not game.check_win_condition():
        player_id = game.current_turn % 2
        player_pieces_positions = [(row, col) for row in range(8) for col in range(8)
                            if game.board[row][col] is not None and
                            game.board[row][col] in game.players[player_id].pieces]

        # Determine the home square row and column based on player_id
        home_square_row, home_square_col = (7, 0) if player_id == 0 else (0, 7)

        # Automatically select 'spawn' if the player has no pieces on the board
        if not player_pieces_positions:
            print("You have no pieces on the board. Automatically selecting 'spawn' for your action.")
            action = "spawn"
        # Automatically select 'move' if the home square is occupied
        elif game.board[home_square_row][home_square_col] in game.players[player_id].pieces:
            print("Your home square is occupied. Automatically selecting 'move' for your action.")
            action = "move"
        else:
            action = input(f"Player {player_id + 1}, choose your action (move/spawn): ").strip().lower()


        if action == "move":
            moves_made = 0
            while moves_made < 3:
                player_pieces_positions = [(row, col) for row in range(8) for col in range(8)
                                           if game.board[row][col] is not None and
                                           game.board[row][col] in game.players[player_id].pieces]

                if len(player_pieces_positions) == 1:
                    # Automatically select the only piece
                    from_row, from_col = player_pieces_positions[0]
                    print(f"Automatically selected your only piece at {chr(from_col + 65)}{8 - from_row}.")
                else:
                    positions_formatted = ', '.join([f"({chr(col + 65)}{8 - row})" for row, col in player_pieces_positions])
                    from_pos = input(f"Move {moves_made + 1}: Enter the position of the piece you want to move (pieces are at: {positions_formatted}): ")

                    if not is_valid_position(from_pos):
                        print("Invalid position. Please use the format 'LetterNumber', e.g., 'B3'.")
                        continue

                    from_row, from_col = 8 - int(from_pos[1]), ord(from_pos[0].upper()) - ord('A')

                    if (from_row, from_col) not in player_pieces_positions:
                        print("You don't have a piece at the chosen position.")
                        continue

                to_pos = input(f"Move {moves_made + 1}: Enter the position to move to (e.g., 'B4'): ")

                if not is_valid_position(to_pos):
                    print("Invalid position. Please use the format 'LetterNumber', e.g., 'B3'.")
                    continue

                to_row, to_col = 8 - int(to_pos[1]), ord(to_pos[0].upper()) - ord('A')
                if game.move_piece(player_id, (from_row, from_col), (to_row, to_col)):
                    moves_made += 1
                else:
                    print("Move was not successful. Please try a different move.")

                if moves_made < 3:
                    game.display_board()

        elif action == "spawn":
            if len(game.players[player_id].pieces) >= 3:
                print("Maximum pieces on board reached. You cannot spawn more pieces.")
                continue

            piece_type = input("Enter the type of piece to spawn (Paper, Scissors, Rock): ").capitalize()
            if piece_type not in ["Paper", "Scissors", "Rock"]:
                print("Invalid piece type. Please choose between Paper, Scissors, and Rock.")
                continue

            game.spawn_piece(player_id, piece_type)
            print("Piece spawned successfully.")
        else:
            print("Invalid action. Please choose 'move' or 'spawn'.")
            continue

        game.display_board()
        game.current_turn += 1
        if game.check_win_condition():
            print(f"Player {player_id + 1} wins!")
            break

run_game_console()

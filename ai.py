import random

class AIAgent:
    def __init__(self, ai_role):
        self.ai_role = ai_role

    def decide_spawn_or_move(self, board_state):
        ai_pieces = self.count_ai_pieces(board_state)
        # Conditions for spawning
        if ai_pieces < 3 and not self.is_home_square_occupied(board_state):
            piece_types = ['paper', 'scissors', 'rock']
            chosen_type = random.choice(piece_types)
            print(f'Only {ai_pieces} belong to AI, choosing to spawn a {chosen_type}')
            return 'spawn', chosen_type
        else:
            # Make a move
            return self.decide_move(board_state)

    def count_ai_pieces(self, board_state):
        count = 0
        for row in board_state:
            for piece in row:
                if piece and piece['player'] == self.ai_role:
                    count += 1
        return count

    def is_home_square_occupied(self, board_state):
        home_square = (0, 7) if self.ai_role == 2 else (7, 0)
        piece = board_state[home_square[0]][home_square[1]]
        return piece and piece['player'] == self.ai_role


    def decide_move(self, board_state):
        ai_pieces = self.get_ai_pieces_with_positions(board_state)
        opponent_home_square = (7, 0) if self.ai_role == 2 else (0, 7)
        best_moves = []

        for piece, row, col in ai_pieces:
            current_distance = abs(row - opponent_home_square[0]) + abs(col - opponent_home_square[1])
            potential_moves = self.get_valid_moves(piece, row, col, board_state, opponent_home_square)
            for move in potential_moves:
                _, (to_row, to_col) = move
                # Calculate Manhattan distance to the opponent's home square for the potential move
                new_distance = abs(to_row - opponent_home_square[0]) + abs(to_col - opponent_home_square[1])

                # Check if the new distance is less than the current distance, indicating a move closer to the opponent's home
                if new_distance < current_distance:
                    best_moves.append(move)  # Add this move to the list of best moves since it brings the piece closer

        if best_moves:
            # Select a move at random from the list of best moves that decrease the distance
            return 'move', random.choice(best_moves)
        else:
            # Handle the case where no move brings a piece closer
            # This could be staying in place, or you might want to consider other strategies
            pass

    def get_ai_pieces_with_positions(self, board_state):
        ai_pieces = []
        for row_idx, row in enumerate(board_state):
            for col_idx, piece in enumerate(row):
                if piece and piece['player'] == self.ai_role:
                    ai_pieces.append((piece, row_idx, col_idx))
        return ai_pieces

    def get_valid_moves(self, piece, row, col, board_state, opponent_home_square):
        potential_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Ensure within board boundaries
                target_square = board_state[new_row][new_col]
                # Check if the square is empty or occupied by an opponent's piece that does not result in a loss
                if not target_square or (target_square['player'] != self.ai_role and ('type' not in target_square or not self.will_lose(piece['type'], target_square.get('type', 'Unknown')))):
                    potential_moves.append(((row, col), (new_row, new_col)))

        return potential_moves

    def will_lose(self, attacker_type, defender_type):
        """Returns True if the attacker will lose against the defender, False otherwise."""
        defeats = {'Rock': 'Paper', 'Paper': 'Scissors', 'Scissors': 'Rock'}
        return defeats[attacker_type] == defender_type

    def simple_ai_decision(self, board_state):
        print(board_state)
        # Placeholder AI logic
        # Return decision as ('spawn', 'Rock') or [('move', from_pos, to_pos), ...]
        fromTo = ((1,6),(2,5))
        return 'move', fromTo
    
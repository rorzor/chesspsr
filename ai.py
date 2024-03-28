import random

class AIAgent:
    def __init__(self, ai_role):
        self.ai_role = ai_role

    def decision(self, board_state, move_count):
        # Step 1: Check for AI Win Possibility
        win_move = self.check_for_win(board_state, move_count)
        if win_move:
            print('I am about to win!')
            return 'move', win_move

        # Step 2: Prevent AI Loss
        prevent_loss_move = self.prevent_loss(board_state, move_count)
        if prevent_loss_move:
            print('Oh no! I hope I dont lose')
            return prevent_loss_move

        # # Step 3: Capture Opponent's Revealed Piece
        # capture_move = self.capture_revealed_opponent_piece(board_state, move_count)
        # if capture_move:
        #     return 'move', capture_move

        # Step 4: Otherwise carry out previous rudimentary logic to further board state in favour of AI
        ai_pieces = self.count_ai_pieces(board_state)
        # Conditions for spawning random piece
        if ai_pieces < 3 and not self.is_home_square_occupied(board_state):
            piece_types = ['Paper', 'Scissors', 'Rock']
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
            potential_moves = self.get_valid_moves(piece, row, col, board_state)
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

    def check_for_win(self, board_state, move_count):
        opponent_home_square = (7, 0) if self.ai_role == 2 else (0, 7)
        ai_pieces = self.get_ai_pieces_with_positions(board_state)

        for piece, row, col in ai_pieces:
            path = self.find_path_to_home(piece, row, col, board_state, opponent_home_square, 3 - move_count)
            if path:
                # If a path is found, return the first move of this path
                return path[0]  # Assuming path[0] is in format ((from_row, from_col), (to_row, to_col))

        # If no winning path is found
        return None

    def find_path_to_home(self, piece, start_row, start_col, board_state, home_square, moves_left, path=[]):
        # Base case: reached the home square or no moves left
        if (start_row, start_col) == home_square:
            return path
        if moves_left == 0:
            return None

        potential_moves = self.get_valid_moves(piece, start_row, start_col, board_state)
        for move in potential_moves:
            _, (next_row, next_col) = move
            new_path = path + [move]
            result = self.find_path_to_home(piece, next_row, next_col, board_state, home_square, moves_left - 1, new_path)
            if result:
                return result

        # If no path can be found within the given moves
        return None

    def get_ai_pieces_with_positions(self, board_state):
        ai_pieces = []
        for row_idx, row in enumerate(board_state):
            for col_idx, piece in enumerate(row):
                if piece and piece['player'] == self.ai_role:
                    ai_pieces.append((piece, row_idx, col_idx))
        return ai_pieces

    def get_valid_moves(self, piece, row, col, board_state):
        piece_owner = piece['player']
        potential_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Ensure within board boundaries
                target_square = board_state[new_row][new_col]
                if not target_square:
                    # The square is empty, so add it as a valid move.
                    potential_moves.append(((row, col), (new_row, new_col)))
                elif target_square['player'] != piece_owner and 'type' in target_square and target_square['type'] != 'Unknown' and piece['type'] != 'Unknown':
                    # The square is occupied by an opponent's piece with a known type, and the AI's piece is also revealed.
                    if not self.will_lose(piece['type'], target_square['type']):
                        potential_moves.append(((row, col), (new_row, new_col)))

        return potential_moves


    def will_lose(self, attacker_type, defender_type):
        """Returns True if the attacker will lose against the defender, False otherwise."""
        defeats = {'Rock': 'Paper', 'Paper': 'Scissors', 'Scissors': 'Rock'}
        return defeats[attacker_type] == defender_type

    def prevent_loss(self, board_state, move_count):
        # Determine how many moves the AI can make this turn
        moves_left = 3 - move_count

        # Locate opponent pieces and their potential paths
        opponent_pieces = self.get_opponent_pieces_with_positions(board_state)
        ai_home_square = (7, 0) if self.ai_role == 1 else (0, 7)
        potential_threats = []

        for piece, row, col in opponent_pieces:
            if self.find_path_to_home(piece, row, col, board_state, ai_home_square, 3):  # Opponent gets 3 moves next turn
                potential_threats.append((piece, row, col))

        # If there's a direct threat, determine the best course of action
        if potential_threats:
            print('Uh oh - trouble')
            for threat in potential_threats:
                # Check if spawning a new piece can block the threat
                if not self.is_home_square_occupied(board_state) and len(self.get_ai_pieces_with_positions(board_state)) < 3:
                    piece_types = ['Paper', 'Scissors', 'Rock']  # Assuming a simple counter system
                    for type in piece_types:
                        if not self.will_lose(type, threat[0]['type']):  # Check if spawning this piece will block the opponent
                            return 'spawn', type

                # Move an existing piece to block or capture the threatening piece
                print('I will try to block')
                block_move = self.find_block_move(board_state, threat, ai_home_square)
                if block_move:
                    return 'move', block_move

        return None

    def find_block_move(self, board_state, threat, ai_home_square):
        print('trying to understand path')
        # Step 1: Determine the path of the threat to the AI's home square
        path_to_block = self.calculate_path_to_block(threat, ai_home_square, board_state)
        print(path_to_block)
        # Step 2: Attempt to Attack the Threat
        for ai_piece in self.get_ai_pieces_with_positions(board_state):
            piece, row, col = ai_piece
            # If the threat is on the path and the AI piece can win, choose to attack
            if (row, col) in path_to_block and 'type' in piece and piece['type'] != 'Unknown' and not self.will_lose(piece['type'], threat['type']):
                print('I think I can stop the attacker!')
                return 'move', ((row, col), threat['position'])  # Move to attack the threat

        # Step 3 & 4: Block the Path
        for ai_piece in self.get_ai_pieces_with_positions(board_state):
            piece, row, col = ai_piece
            # Find the nearest piece that can move into the path
            for move in self.get_valid_moves(piece, row, col, board_state):
                _, (to_row, to_col) = move
                if (to_row, to_col) in path_to_block:
                    # Move to block the path if it's an AI piece not revealed or if the threat cannot defeat it
                    if piece['type'] == 'Unknown' or not self.will_lose(piece['type'], threat.get('type', 'Unknown')):
                        print('I cant let you do that, Dave')
                        return 'move', ((row, col), (to_row, to_col))

        # If no block move is found, return None or some default action
        return None
    
    def calculate_path_to_block(self, threat, ai_home_square, board_state):
        path_to_home = []
        # Assuming threat is a tuple like (piece, row, col)
        _, threat_row, threat_col = threat

        # Generate direct path(s) to home square
        # Vertical path
        if threat_row != ai_home_square[0]:
            step = 1 if threat_row < ai_home_square[0] else -1
            for row in range(threat_row, ai_home_square[0], step):
                path_to_home.append((row, threat_col))
        
        # Horizontal path
        if threat_col != ai_home_square[1]:
            step = 1 if threat_col < ai_home_square[1] else -1
            for col in range(threat_col, ai_home_square[1], step):
                path_to_home.append((threat_row, col))

        return path_to_home



    def get_opponent_pieces_with_positions(self, board_state):
        opponent_pieces = []
        for row_idx, row in enumerate(board_state):
            for col_idx, piece in enumerate(row):
                if piece and piece['player'] != self.ai_role:
                    opponent_pieces.append((piece, row_idx, col_idx))
        return opponent_pieces

    # Derp. A simple move to test an AI making a move
    def simple_ai_decision(self, board_state):
        print(board_state)
        # Placeholder AI logic
        # Return decision as ('spawn', 'Rock') or [('move', from_pos, to_pos), ...]
        fromTo = ((1,6),(2,5))
        return 'move', fromTo
    
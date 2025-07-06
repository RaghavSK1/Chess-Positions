import basic_chess as bc

# This function should be taken from task 6
def read_pgn(file_name: str) -> list[dict]:
    """
    This function reads the games contained in the file into a list of dictionaries (containing the games)

    Arguments:
        file_name (str) : the name of the pgn file_name
    
    Returns:
        list[dict]: A list where each element is a game, formatted as a dictionary
    """
    # Create an empty list to hold the different game data (as dictionaries)
    all_games = []
    
    with open(file_name, "r") as pgn_file:
        file_string = pgn_file.read().strip()
    
    # Split the whole file (as a string) where there is a blank line 
    # This stores tags in one element and moves in the next element
    file_parts = file_string.split("\n\n")
    
    # Iterate through the file parts (2 at a time) and read the tags and moves of each game
    for i in range(0, len(file_parts) - 1, 2):
        single_game_data = read_single_game(file_parts[i], file_parts[i+1])
        all_games.append(single_game_data)
    
    return all_games

def read_single_game(tag_info: str, moves: str) -> dict:
    """
    Reads a single game's 'tags and moves' into a dictionary

    Arguments:
        tag_info (str): all the tags and their info (start of each game)
        moves (str): all the moves played for the game 
    
    Returns:
        dict: Dictionary containing the game data
    """
    # Initialise the game data with the tags
    game_data = {
        "event": "-",
        "white": "-",
        "black": "-",
        "result": "-",
        "whiteelo": "-",
        "blackelo": "-",
        "opening": "-",
    }

    for tag_line in tag_info.splitlines():
        # Remove the outer brackets, quotation marks and split at the first space
        tag_line = tag_line.strip("[]").replace('"', '')
        tag_line_parts = tag_line.split(" ",1)

        key, information = tag_line_parts

        # If the key was initialised as a tag, add its information to the dictionary
        if (key.lower() in game_data):
            game_data[key.lower()] = information
    
    # Initialise all the moves in the dictionary to be "-"
    for i in range(1,41):

        # If i is odd, then add a white move key 
        if (i % 2 == 1):
            # Floor division then adding 1 ensures the corresponding white move
            game_data[f"w{i//2 + 1}"] = "-"
        
        # Otherwise add a black move key
        else:
            game_data[f"b{i//2}"] = "-"

    move_list = moves.strip().split(" ")

    # For each element in move_list, if it is the move number, add the white and black moves to the dictionary
    move_number = 1

    for i, move in enumerate(move_list):
        if move_number > 20:
            break

        elif move == f"{move_number}.":
            # Add the white and black move if it is not the result (final element)
            if move_list[i+1] != game_data["result"]:
                game_data[f"w{move_number}"] = move_list[i+1]

            if move_list[i+2] != game_data["result"]:
                game_data[f"b{move_number}"] = move_list[i+2]
            
            # Increment the move_number if the move is registered
            move_number += 1
    
    return game_data


#Part 1
def count_positions(moves: list[str], depth: int) -> int:
    """
    Returns the total number of legal moves at a specified distance from the current position.
    Uses recursion to calculate the total number of moves from one level of depth lower until a depth of 1 is reached (which can be caluclated using Binh's function)

    Arguments:
        moves (list[str]): List of moves that have been played
        depth (int): The distance from the current position to look for
    
    Returns:
        int: Total number of moves at the specified depth
    """

    total_legal_moves = 0
    
    # Base case where depth is 1
    if depth <= 1:
        total_legal_moves = len(bc.possible_moves(moves))
    
    # Otherwise if depth > 1
    else:
        
        # Iterate through each possible move being added to moves and calculate the number of moves from there
        for possible_move in bc.possible_moves(moves):
            new_moves_played = moves + [possible_move]
            new_depth = depth - 1
            
            # Recursively adds the number of positions by decreasing depth (by 1) and adding a possible move
            total_legal_moves += count_positions(new_moves_played, new_depth)

    return total_legal_moves

#Part 2
def winning_statistics(file_name: str, depth: int, tolerance: int) -> tuple[float, list[str], int]:
    """
    Given a file, depth and the tolerance (minimum number of games that match the move sequence), the function returns a tuple containing the highest probability for white to win, the set of moves for that probability and the total number of games that followed the moves.

    Arguments:
        file_name (str): the name of the pgn file containing chess games
        depth (int): the depth to search moves for
        tolerance (int): the total number of games that must follow the move sequence
    
    Returns:
        float: The highest probability white wins from the move sequence
        list[str]: The sequence of moves with highest white win probability
        int: The number of games where the move sequence was played
    """
    
    # First read the file into list then pass the list into a recursive function
    all_games = read_pgn(file_name)

    return find_best_moves(all_games, [], depth, tolerance)

def find_best_moves(games: list[dict], moves: list[str], depth: int, tolerance: int):
    """
    Given chess games played, depth and the tolerance (minimum number of games that match the move sequence), the function returns a tuple containing the highest probability for white to win, the set of moves for that probability and the total number of games that followed the moves.

    Arguments:
        games (list[dict]): The chess games formatted as a list of dictionaries
        moves (list[str]): The move sequence that have been made (updates recursively)
        depth (int): the depth to search moves for (updates recursively)
        tolerance (int): the total number of games that must follow the move sequence
    
    Returns:
        float: The highest probability white wins from the move sequence
        list[str]: The sequence of moves with highest white win probability
        int: The number of games where the move sequence was played
    """
    # Gets number of white/black wins and draws for moves sequence
    white_wins, black_wins, draws = win_loss_by_moves(games, moves)

    # Since all games must have white winning, black winning or draw, the sum is the total games
    total_games = white_wins + black_wins + draws

    # Initialise the probability white wins to 0
    probability_white_win = 0

    # First check games at the position exist before calculating white win probability
    if total_games > 0:
        probability_white_win = white_wins/total_games
    
    # Base case: when depth = 0
    if depth < 1:
        # If there are enough games at the position, return the statistics
        if total_games >= tolerance:
            return probability_white_win, moves, total_games
        
        # Otherwise this sequence of moves gets disregarded (it has 0 white win probability)
        else: 
            return 0, [], 0
    
    else:
        # Holds the possible move sequences from current position
        possible_sequences = []

        for possible_move in bc.possible_moves(moves):
            # Add the possible move and update depth
            new_moves_played = moves + [possible_move]
            new_depth = depth - 1

            # Adds the new best move sequence from the possible position
            possible_sequences.append(find_best_moves(games, new_moves_played, new_depth, tolerance))
        
        # Find highest probability move sequence
        best_sequence = (0,[],0)
        for sequence in possible_sequences:
            # If any sequence has a better probability, update the best sequence
            if sequence[0] > best_sequence[0]:
                best_sequence = sequence
        
        return best_sequence


# Extension of task 6 function - now includes draws as well
def win_loss_by_moves(games: list[dict], moves: list[str]) -> tuple[int, int, int]:
    """
    From a list of games and a list of moves, this function determines the number of games won by white/black for the same moves. 

    Arguments:
        games (list[dict]): All games played with tags and moves 
        moves (list[str]): The list of valid chess moves to analyse
    
    Returns:
        tuple[int, int, int]: Indicates number of wins by white, number of wins by black from those moves, number of draws
    """
    white_wins = 0
    black_wins = 0
    draws = 0

    # Check whether each game follows the move sequence, and record its result if it does
    for game in games:
        if check_game_following_moves(game, moves):
            result = game["result"]
            
            # Increment the 'white wins'/'black wins'/'draws' depending on result
            if result == "1-0":
                white_wins += 1
            
            elif result == "0-1":
                black_wins += 1
            
            else:
                draws += 1
    
    return white_wins, black_wins, draws
    
def check_game_following_moves(game: dict, moves: list[str]) -> bool:
    """
    Checks whether a single game is following a list of moves.

    Arguments:
        game (dict): The game played (containing tag and move kets)
        moves (list[str]): The list of chess moves that is checked if it was played in the game
    
    Returns:
        bool: True or False depending on whether or not the game follows the moves
    """

    # Stores the total move number (for both black and white)
    total_move_number = 1
    game_follows_moves = True
        
    for move in moves:
        # No more moves to check (20 white + 20 black)
        if total_move_number >= 40:
            break
        
        # If it is a white move
        if total_move_number % 2 == 1:
            # Disregard the result if game doesn't follow the move
            if move != game[f"w{total_move_number//2 + 1}"]:
                game_follows_moves = False
                break
        
        # Otherwise, it is a black move
        else:
            if move != game[f"b{total_move_number//2}"]:
                game_follows_moves = False
                break
        
        # Increment move number before moving onto next move
        total_move_number += 1
    
    return game_follows_moves
# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your test code goes here
    print(winning_statistics("lichess_small.pgn", 1, 10))

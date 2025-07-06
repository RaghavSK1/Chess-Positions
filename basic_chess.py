import sys
sys.path.append('/course/')

import chess

def possible_moves(moves: list[str]) -> list[str]:
    """
    Returns a list of all legal next moves from the given board position 
    in Standard Algebraic Notation (SAN).

    Args:
        moves (list[str]): A list of moves in SAN to apply to the starting position.

    Returns:
        list[str]: A list of legal next moves in SAN from the resulting position.
    """
    board = chess.Board()  # Initialize a new chess board

    # Apply each move in the list to update the board position
    for move in moves:
        board.push_san(move)

    # Convert all legal moves to SAN and return them
    return [board.san(move) for move in board.legal_moves]


def show_board(moves: list[str]) -> str:
    """
    Returns a string representation of the chess board after applying 
    the given moves.

    Args:
        moves (list[str]): A list of moves in SAN to apply to the starting position.

    Returns:
        str: An ASCII string representation of the board.
    """
    board = chess.Board()  # Initialize a new chess board

    # Apply each move to update the board
    for move in moves:
        board.push_san(move)

    return str(board)  # Return the board as a string

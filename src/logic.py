import random
from typing import List, Dict

import tools

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""


def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "daedalean",  # TODO: Your Battlesnake Username
        "color": "#3E338F",  # TODO: Personalize
        "head": "pixel",  # TODO: Personalize
        "tail": "pixel",  # TODO: Personalize
        "version": "0.0.1-beta",
    }


def choose_start(data: dict) -> None:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: None.

    Use the information in 'data' to initialize your next game. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    pass


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]  # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake[
        "body"
    ]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Step 0: Don't allow your Battlesnake to move back on it's own neck.
    possible_moves = _avoid_my_neck(my_body, possible_moves)

    # TODO: Step 1 - Don't hit walls.
    # Use information from `data` and `my_head` to not move beyond the game board.
    board = data['board']
    board_height = board['height']
    board_width = board['width']
    possible_moves = _avoid_hitting_walls(
        my_body, possible_moves, board_height, board_width, data
    )

    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.
    possible_moves = _avoid_hitting_myself(my_body, possible_moves)

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.
    possible_moves = _avoid_colliding_others(my_body, possible_moves, data)

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    # move = random.choice(possible_moves) if possible_moves else "up"
    # TODO: Explore new strategies for picking a move that are better than random
    if possible_moves:
        move = random.choice(possible_moves)
    else:
        move = "up"

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}"
    )

    return move


def _avoid_my_neck(my_body: dict, possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves


def _avoid_hitting_walls(
    my_body: dict,
    possible_moves: List[str],
    board_height: int,
    board_width: int,
    data: dict,
) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: The list of remaining possible_moves, with 'wall' directions removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    game_type = tools.get_game_type(data)

    if game_type != "wrapped":
        possible_move_set = tools.get_possible_move_set(possible_moves)
        adjacent_squares_and_moves = tools.get_adjacent_squares_and_moves(my_head)

        for adjacent_square, move in adjacent_squares_and_moves:
            out_of_bounds = tools.is_out_of_bounds(
                adjacent_square, board_height, board_width
            )
            if out_of_bounds and move in possible_move_set:
                possible_moves.remove(move)

    return possible_moves


def _avoid_hitting_myself(my_body: dict, possible_moves: List[str]) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with 'body' directions removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    body_set_except_tail = tools.get_body_set_except_tail(my_body)
    possible_move_set = tools.get_possible_move_set(possible_moves)

    adjacent_squares_and_moves = tools.get_adjacent_squares_and_moves(my_head)

    for adjacent_square, move in adjacent_squares_and_moves:
        if adjacent_square in body_set_except_tail and move in possible_move_set:
            possible_moves.remove(move)

    return possible_moves


def _avoid_colliding_others(
    my_body: dict, possible_moves: List[str], data: dict
) -> List[str]:
    """
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
            For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: The list of remaining possible_moves, with 'others' directions removed
    """
    my_head = my_body[0]  # The first body coordinate is always the head
    other_body_set_except_squadmates_and_tails = (
        tools.get_other_body_set_except_squadmates_and_tails(data)
    )
    possible_move_set = tools.get_possible_move_set(possible_moves)

    adjacent_squares_and_moves = tools.get_adjacent_squares_and_moves(my_head)

    for adjacent_square, move in adjacent_squares_and_moves:
        if (
            adjacent_square in other_body_set_except_squadmates_and_tails
            and move in possible_move_set
        ):
            possible_moves.remove(move)

    return possible_moves


def choose_shout(data: dict, move: str) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    move: A String, the single move to make. One of "up", "down", "left" or "right".

    return: A String, the single shout to make.

    Use the information in 'data' and 'move' to decide your next shout. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    shouts = [
        "why are we shouting??",
        "I'm not really sure...",
        f"I guess I'll go {move} then.",
    ]
    shout = random.choice(shouts)
    return shout


def choose_end(data: dict) -> None:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: None.

    Use the information in 'data' to delete your previous game. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    pass

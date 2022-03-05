import curses
import pickle
import re
from typing import Tuple, Optional
from pathlib import Path

import typer
import random
from curses import wrapper
from string import ascii_lowercase

from battleship import MESSAGE_HEIGHT, LEGEND_MENU_HEIGHT, Battleship
from field import MIN_LENGTH, MAX_LENGTH, MIN_WIDTH, MAX_WIDTH

INPUT_MESSAGE = 'Enter command: '
INPUT_HEIGHT = 1
INPUT_WIDTH = len(INPUT_MESSAGE) + 3

SAVINGS_DIRECTORY = Path('.') / 'savings'


def parse_point(s: str) -> Tuple[int, int]:
    """
    Check that string beginning has form '1 letter and 1-2 digits' and
    parse it as coordinates on battleship field.
    :param s: user input
    :return: coordinates greater 0 on success or (-1, -1) on failure
    """
    if len(s) == 2 and re.match(r'[a-zA-Z]\d', s):
        # s has form like 'a5' or 'B0'
        x = ascii_lowercase.index(s[0].lower())
        y = int(s[1]) - 1
        return x, y
    elif len(s) == 3 and re.match(r'[a-zA-Z]\d{2}', s):
        # # s has form like 'a25' or 'B99'
        x = ascii_lowercase.index(s[0].lower())
        y = int(s[1]) * 10 + int(s[2]) - 1
        return x, y
    else:
        return -1, -1


def save_game(game: Battleship):
    """
    Try to save given game into a file in form 'SAVINGS_DIRECTORY/length_width'
    :param game: current game object
    """
    if not SAVINGS_DIRECTORY.exists():
        SAVINGS_DIRECTORY.mkdir()
    try:
        with open(SAVINGS_DIRECTORY / f'{game.field_length}_{game.field_width}', 'wb') as file:
            pickle.dump(game, file)
    except IOError:
        # Ignore error
        pass


def random_shot_generator(field_length: int, field_width: int):
    """
    Generator of random shots for computer player
    :param field_length: length of game field
    :param field_width: width of game field
    :return: generator of points (x, y) within the field
    """
    points = [(x, y) for x in range(field_length) for y in range(field_width)]
    random.shuffle(points)
    for x, y in points:
        yield x, y


def play(screen: curses.window, game: Battleship):
    """
    Simulates a game of Battleship.
    When ':q' is entered try to save current session and then exit.
    :param screen: window object
    :param game: current game object
    """
    # Enable echoing character input to the screen as it is entered.
    curses.echo()

    # Create generator of random shots
    shot_generator = random_shot_generator(game.field_length, game.field_width)

    while True:
        # Clear screen
        screen.clear()

        # Required height and width of the screen
        required_height = game.host_field_height + 1 + LEGEND_MENU_HEIGHT + 1 + MESSAGE_HEIGHT + 1 + INPUT_HEIGHT
        required_width = max(game.width_on_screen, INPUT_WIDTH) + 2

        # Check if screen is large enough to play game
        screen_height, screen_width = screen.getmaxyx()
        if screen_height < required_height or screen_width < required_width:
            screen.addstr(0, 0, 'Please make your terminal screen larger.\n')
            # Optimize screen drawing
            screen.getch()
            continue

        # Calculate y-values for the strings we want to display
        # We want 1 newline between each of the strings
        legend_menu_y = game.host_field_height + 1
        message_y = legend_menu_y + LEGEND_MENU_HEIGHT + 1
        input_y = message_y + MESSAGE_HEIGHT + 1

        # Calculate x-value of input string
        input_x = (screen_width - INPUT_WIDTH) // 2

        # Display information strings on screen
        screen.addstr(0, 0, game.display_host_field(screen_width))
        screen.addstr(legend_menu_y, 0, game.display_host_legend_menu(screen_width))
        screen.addstr(message_y, 0, game.display_host_message(screen_width))
        screen.addstr(input_y, input_x, INPUT_MESSAGE)

        if game.turn == game.host:
            # Get user input
            s = screen.getstr(input_y, input_x + len(INPUT_MESSAGE), 3).decode(encoding='utf-8')
            if s == ':q':
                save_game(game)
                break
            if len(s) < 2:
                # len(s) must be 2 or 3
                continue
            game.make_shot(*parse_point(s))
        else:
            # Make random shot
            game.make_shot(*next(shot_generator))


def load_game(field_length: int, field_width: int) -> Optional[Battleship]:
    """
    Try to load last saving for game with the same field sizes
    :param field_length: length of game field
    :param field_width: width of game field
    :return: game object on success or None on failure
    """
    try:
        with open(SAVINGS_DIRECTORY / f'{field_length}_{field_width}', 'rb') as file:
            return pickle.load(file)
    except IOError:
        # Ignore error
        return None


def start_game(screen, field_length: int, field_width: int):
    # Clear screen
    screen.clear()

    message_str = '\n'

    while True:
        greeting = '#######################################\n' \
                   + '#        WELCOME TO BATTLESHIP        #\n' \
                   + '#######################################\n\n'

        instructions_str = '\nPress p to play a new game.\nPress l to load previous game.\nPress q to quit.'

        # Display instructions and message on screen
        screen.clear()
        screen.addstr(0, 0, greeting + message_str + instructions_str)

        # Get user input
        c = screen.getch()
        if c == ord('q'):
            # Quit the game
            return
        elif c == ord('l'):
            # Load saving
            game = load_game(field_length, field_width)
            if game is not None:
                # Run loaded game
                play(screen, game)
                message_str = "\n"
            else:
                # Failed to load game
                message_str = 'Failed to load last saving.\n'
        elif c == ord('p'):
            # Play a new game
            game = Battleship(field_length, field_width)
            play(screen, game)
            # Clear message string
            message_str = "\n"


def length_callback(value: int) -> int:
    """
    Check that given field length is within range [MIN_LENGTH; MAX_LENGTH] and raise error if it is not
    :param value: field length
    :return: given value
    """
    if not MIN_LENGTH <= value <= MAX_LENGTH:
        raise typer.BadParameter(f'Field length must be in range [{MIN_LENGTH}; {MAX_LENGTH}], '
                                 f'actually: {value}')
    return value


def width_callback(value: int):
    """
    Check that given field width is within range [MIN_WIDTH; MAX_WIDTH] and raise error if it is not
    :param value: field width
    :return: given value
    """
    if not MIN_WIDTH <= value <= MAX_WIDTH:
        raise typer.BadParameter(f'Field width must be in range [{MIN_WIDTH}; {MAX_WIDTH}], '
                                 f'actually: {value}')
    return value


def main(field_length: int = typer.Option(MIN_LENGTH, callback=length_callback),
         field_width: int = typer.Option(MIN_WIDTH, callback=width_callback)):
    wrapper(start_game, field_length, field_width)


if __name__ == '__main__':
    typer.run(main)

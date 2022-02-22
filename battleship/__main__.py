import curses

import typer
import random
from curses import wrapper
from string import ascii_lowercase, ascii_letters

from battleship import Battleship
from table import MIN_LENGTH, MAX_LENGTH, MIN_WIDTH, MAX_WIDTH


def play(screen: curses.window, game: Battleship):
    """
    Simulates a game of Battleship.
    The game ends with a winner or when "q" is pressed.
    """
    while True:
        # Clear screen
        screen.clear()
        # Enable echoing character input to the screen as it is entered.
        curses.echo()

        required_height = game.field_height + 1 + game.menu_height + 1 + game.message_height + 2

        # Check if screen is large enough to play game
        screen_height, screen_width = screen.getmaxyx()
        if screen_height < required_height:
            screen.addstr(0, 0, "Please make your terminal screen larger.")
            continue

        # Check if a player has won.
        if game.winner is not None:
            break

        # Calculate y-values for the strings we want to display
        # We want 1 newline between each of the strings
        menu_y = game.field_height + 1
        message_y = menu_y + game.menu_height + 1
        input_y = message_y + game.message_height + 1

        input_x = (screen_width - len("Enter point to shot: ") - 2) // 2

        # Display information strings on screen
        screen.addstr(0, 0, game.players[0].display_field(screen_width))
        screen.addstr(menu_y, 0, game.display_menu(screen_width))
        screen.addstr(message_y, 0, game.display_message(screen_width))
        screen.addstr(input_y, input_x, "Enter point to shot: ")

        numbers = [str(i) for i in range(1, game.field_width + 1)]

        if game.turn == 0:
            # Get user input
            s = screen.getstr(input_y, input_x + len("Enter point to shot: "), 2).decode(encoding="utf-8")
            if len(s) == 2 and s[0] in ascii_letters and s[1] in numbers:
                x = ascii_lowercase.index(s[0].lower())
                y = int(s[1]) - 1
                game.make_shot(x, y)
        else:
            x, y = random.randint(0, game.field_length - 1), random.randint(0, game.field_width - 1)
            game.make_shot(x, y)


def start_game(screen, field_length: int, field_width: int):
    # Clear screen
    screen.clear()
    # Initialize the game
    game = Battleship(field_length, field_width)

    while True:
        greeting = '#######################################\n' \
                   + '#        WELCOME TO BATTLESHIP        #\n' \
                   + '#######################################\n\n'
        # TODO add saving and loading !!!!!!!!!
        instructions_str = '\nPress p to play a new game.\nPress q to quit.'
        # Set winner message if player 0 or player 1 won
        winner_str = ''
        if game.winner == 0:
            winner_str = "You are winner!\n"
        elif game.winner == 1:
            winner_str = "You lose!\n"

        # Display instructions and winner message on screen
        screen.clear()
        screen.addstr(0, 0, greeting + winner_str + instructions_str)

        # Get user input
        c = screen.getch()
        if c == ord('q'):
            # Quit the game
            return
        elif c == ord('p'):
            # Play a new game
            game = Battleship(field_length, field_width)
            play(screen, game)


def length_callback(value: int):
    if not MIN_LENGTH <= value <= MAX_LENGTH:
        raise typer.BadParameter(f"Field length must be in range [{MIN_LENGTH}; {MAX_LENGTH}], "
                                 f"actually: {value}")
    return value


def width_callback(value: int):
    if not MIN_WIDTH <= value <= MAX_WIDTH:
        raise typer.BadParameter(f"Field width must be in range [{MIN_WIDTH}; {MAX_WIDTH}], "
                                 f"actually: {value}")
    return value


def main(field_length: int = typer.Option(..., callback=length_callback),
         field_width: int = typer.Option(..., callback=width_callback)):
    wrapper(start_game, field_length, field_width)


if __name__ == "__main__":
    typer.run(main)

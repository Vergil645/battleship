from curses import wrapper
import typer
import random

from battleship import Battleship

# HUMAN_PLAYER_NAME = 'Human'
# COMPUTER_PLAYER_NAME = 'Machine'

# def get_player_name(message):
#     """
#     Returns player name from user input.
#     The name must have 15 or less characters.
#     If no name is entered (empty string), then the name will just be 'Player [player_num]'.
#     """
#     input_message = f"{message}:  "
#     name = input(input_message)
#     # TODO мб убрать ограничение
#     while len(name) > 15:
#         name = input("Please enter a name with 15 or less characters:  ")
#     return name


def play(game, screen):
    """
    Simulates a game of Battleship.
    The game ends with a winner or when "q" is pressed.
    """
    while True:
        # Clear screen
        screen.clear()

        # Check if screen is large enough to play game
        # screen_height, screen_width = screen.getmaxyx()
        # if screen_height < REQUIRED_HEIGHT:
        #     window.addstr(0, 0, "Please make your terminal screen larger.")
        #     continue

        # Check if a player has won.
        if game.winner:
            break

        # Calculate y-values for the strings we want to display
        # We want 1 newline between each of the strings
        # message_y = CARD_HEIGHT + 1
        # player_menus_y = message_y + MESSAGE_HEIGHT + 1
        # current_call_y = player_menus_y + MENU_HEIGHT + 1

        # Display information strings on screen
        # screen.addstr(0, 0, game.top_card_str(screen_width))
        # screen.addstr(message_y, 0, game.message_str(screen_width))
        # screen.addstr(player_menus_y, 0, game.player_menus_str(screen_width))
        # screen.addstr(current_call_y, 0, game.current_rank_str())

        # Get user input
        c = screen.getch()

        # if c in [ord(ch) for ch in ascii_letters] and game.turn == 0:
        #     # human turn
        #     pass
        # elif c in [ord(','), ord('.'), ord('/')] and game.turn == 1:
        #     # Player 1's turn to place a card on the pile
        #     game.play_card(game.current_player)
        # elif c in [ord('a'), ord('s'), ord('d')]:
        #     # Player 0 wants to slap the pile
        #     game.slap_card(0)
        # elif c in [ord('l'), ord(';'), ord("'")]:
        #     # Player 1 wants to slap the pile
        #     game.slap_card(1)
        # elif c == ord('q'):
        #     # Quit this game
        #     return

def play(screen):
    # Clear screen
    screen.clear()
    # Initialize the game
    # game = Battleship()
    #
    # while True:
    #     slapjack_str = '#####################################\n' \
    #                  + '#        WELCOME TO SLAPJACK        #\n' \
    #                  + '#####################################\n\n'
    #     player_names_str = 'Player 1: {}\n'.format(PLAYER_NAME_0)   \
    #                      + 'Player 2: {}\n'.format(PLAYER_NAME_1)
    #     instructions_str = '\nPress p to play a new game.\nPress q to quit.'
    #     # Set winner message if player 0 or player 1 won
    #     winner_str = '{} is the winner!\n'.format(game.winner.name.strip()) if game.winner else ''
    #
    #     # Display instructions and winner message on screen
    #     screen.clear()
    #     screen.addstr(0, 0, slapjack_str + winner_str + instructions_str)
    #
    #     # Get user input
    #     c = screen.getch()
    #     if c == ord('q'):
    #         # Quit the game
    #         return
    #     elif c == ord('p'):
    #         # Play a new game
    #         game = Slapjack(PLAYER_NAME_0, PLAYER_NAME_1)
    #         play(game, screen)


def main(field_length: int, field_width: int):
    # wrapper(play)
    game = Battleship(field_length, field_width)
    while True:
        if game.winner:
            print(str(game.turn) + " wins!")
            return
        if game.turn == 0:
            print(game.players[0].display_str(0))
            x, y = map(int, input("Inter target:  ").split())
            game.make_shot(x - 1, y - 1)
        else:
            x, y = random.randint(0, field_length - 1), random.randint(0, field_width - 1)
            game.make_shot(x, y)


if __name__ == "__main__":
    typer.run(main)
    # print("Playing a game of Battleship...")
    # Ask for user to input names
    # PLAYER_NAME_0 = get_player_name(1) or 'Player 1' # 'Player 1' is represented as Player 0 internally
    # PLAYER_NAME_1 = get_player_name(2) or 'Player 2' # 'Player 2' is represented as Player 1 internally

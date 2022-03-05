# Battleship
> A game of two-player Battleship between human and computer in your console.

### Game Rules
The game is played on four grids, two for each player. The grids are rectangles, the grid are identified by letter and number. On one grid the player arranges ships and records the shots by the opponent. On the other grid the player records their own shots.

Before play begins, each player secretly arranges their ships on their primary grid. Each ship occupies a number of consecutive squares on the grid, arranged either horizontally or vertically. The number of squares for each ship is determined by the type of the ship. The ships cannot overlap (i.e., only one ship can occupy any given square in the grid). The types and numbers of ships allowed are the same for each player.

After the ships have been positioned, the game proceeds in a series of rounds. In each round, each player takes a turn to announce a target square in the opponent's grid which is to be shot at. The opponent announces whether the square is occupied by a ship. If it is a "hit", the player who is hit marks this on their own or "ocean" grid. The attacking player marks the hit or miss on their own "tracking" or "target" grid, in order to build up a picture of the opponent's fleet.

When all the squares of a ship have been hit, the ship's owner announces the sinking of it. If all of a player's ships have been sunk, the game is over and their opponent wins.

##### Requirements
You must have Python 3.8+ to run the game.

##### Run the Game
Navigate to the directory in your console and then run:
```sh
$ python battleship [--field-length <length value>] [--field-width <width value>]
```

##### Keyboard Commands

To play a new game of Battleship, press `p`. To load a previous game with the same field sizes press `l`. To quit the game, press `q`.

When game is running you can type `:q` to save current game and quit.

### Design Decisions

I created separate `Ship`, `Field`, `Player`, and `Battleship` classes to modularize my code. Each of the `Ship`, `Field`, `Player`, and `Battleship` classes store relevant information as instance variables and have methods that generate strings to be displayed on the terminal screen.

The `__main__.py` class is separate from the above classes, and takes care of user input and rendering the game logic as information on the terminal screen.

##### External Python Libraries Used
* `curses`
* `typer`

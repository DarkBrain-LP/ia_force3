# IA Force3

To use this project, follow the steps below:

1. Install the required dependencies by running the following command:
    ```shell
    pip install flet
    ```

2. Run the `force3.py` file to execute the main program.

3. The AI implementation of this project can be found in the `model.py` file.

4. The user interface components are located in the `ui` folder.

## Force 3
Force 3 Game

Number of players: 2
Equipment:
- Square board with 9 squares
- 6 round pieces (3 of one color and 3 of another)
- 8 square pieces of a light color
Objective of the game:
Align three of your round pieces horizontally, vertically, or diagonally.
Game Description:
The 8 square pieces are arranged on the board around the central square. Players use the round pieces by each choosing a color before starting to play. They take turns making one of the following three moves:
- Placing a round piece on an unoccupied square,
- Sliding a square (occupied or not by a round piece) to an empty square,
- Moving an already-placed round piece to any empty square.
If the empty square is at the edge of the board, the player can move two squares in one turn. Their opponent is not allowed to make the opposite move in the next turn to return the squares to their initial position. However, they can move only one square. The first player to align their three pieces wins.
Project Objective:
Allow the user to play Force 3 against the computer. At the beginning of the game, the user must choose whether to play with the white pieces, black pieces, or to watch the computer play against itself.

## AI Implementation

A state is represented by 
- A board (3X3 matrix)
- The empty case position
- The player who is going to play
- The possibility to move two cards horizontally
- The possibility to move two cards vertically

### Resolution
The MiniMax algorithm was implemented to tacle the Force3 game. The alpha bêta prunning is planned to be implemented for a higher performance of the AI

## UI
The flet package was used to implement the UI. Thanks to the flutter widgets, custom components were created to create the board and handle user and AI moves :
- **Slot** : represents the spaces where the **Card** and **Pawn** will not be placed
- **Card** represents the empty squares on which the **Pawn** will be placed
- **Pawn** represents the round game pieces

## TODOs
- refactor the code
- implement the alpha-bêta prunning
- save the scores
- reinforce the AI by making it learn from his previous games 
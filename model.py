"""Jeu Force 3

Nombre de joueurs : 2
Matériel :
– plateau carré de 9 cases
– 6 pions ronds (3 d'une couleur et 3 d'une autre)
– 8 pions carrés de couleur claire
But du jeu :
Aligner ses trois pions ronds horizontalement, verticalement ou en diagonale.
Description du jeu :
Les 8 pions carrés sont disposés sur le plateau autour de la case centrale. Les joueurs utilisent les
pions ronds en choisissant chacun une couleur avant de commencer à jouer. Ils jouent à tour de rôle
en effectuant un des trois mouvements suivants :
– pose d'un pion rond sur un carré inoccupé,
– déplacement par glissement d'un carré (occupé ou non par un pion rond) vers une case vide,
– déplacement d'un pion rond déjà en place vers n'importe quel carré libre.
Si la case vide se trouve au bord du plateau, le joueur peut déplacer deux carrés d'un seul coup. Son
adversaire n'aura pas le droit d'effectuer au tour suivant le mouvement inverse pour remettre les
carrés dans leur position initiale. Il pourra cependant en déplacer un seul. Le premier joueur qui
parvient à aligner ses trois pions a gagné.
Objectif du projet :
Permettre à l'utilisateur de jouer à Force 3 contre l'ordinateur. L'utilisateur devra choisir au début de
la partie s'il désire jouer avec les blancs ou les noirs, ou s'il désire regarder l'ordinateur jouer contre
lui-même.

Keyword arguments:
argument -- description
Return: return_description
"""
class Force3:
    def __init__(self):
        self.empty_case = (1, 1)
        self.current_player = 1
        self.two_case_mv_dir = -1 # represents the direction in which the two case could be moved : -1 if impossible, 0 for horizontal, 1 for vertical
        # -1 represente un carré innocupé, 0 la case vide, 1 un pion du jour 1 et 2 un pion du joueur 2
        self.plateau = [[-1, -1, -1], [-1, 0, -1], [-1, -1, -1]]

    def canMoveTwoCases(x,y):
        if (x,y) in [(0,0), (0,2), (2,0), (2,2)]:
            return 2 # can move horizontally and vertically
        if (x,y) in [(0,1), (2,1)]:
            return 1 # can move vertically
        if (x,y) in [(1,0), (1,2)]:
            return 0 # can move horizontally
        return -1 # can't move
    

    def moveOneCase(self):
        """
        Gets the empty case and return the possible states of the board if the current player moves one case
        """
        x, y = self.empty_case
        possible_states = []
        # clone the board
        # move up
        print(x,y)
        if x <= 1 and x+1 <= 2:
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            new_board[x][y] = new_board[x+1][y]
            new_board[x+1][y] = 0
            possible_states.append(new_board)
        # move down
        if x <= 1 and x-1 >= 0:
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            new_board[x][y] = new_board[x-1][y]
            new_board[x-1][y] = 0
            possible_states.append(new_board)
        # move left
        if y <= 1: # and y+1 <= 2
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            new_board[x][y] = new_board[x][y+1]
            new_board[x][y+1] = 0
            possible_states.append(new_board)
        # move right
        if y >= 1 : #and y-1 >= 0
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            new_board[x][y] = new_board[x][y-1]
            new_board[x][y-1] = 0
            possible_states.append(new_board)
        return possible_states
        
        
    def moveTwoCases(self):
        x, y = self.empty_case
        possible_states = []
        # clone the board
        # move up
        if x == 0:
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            for i in range(2):
                new_board[x+i][y] = new_board[x+i+1][y]
                new_board[x+i+1][y] = 0
            possible_states.append(new_board)
        # move down
        if x == 2:
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            for i in range(2):
                new_board[x-i][y] = new_board[x-i-1][y]
                new_board[x-i-1][y] = 0
            possible_states.append(new_board)
        # move left
        if y == 0:
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            for i in range(2):
                new_board[x][y+i] = new_board[x][y+i+1]
                new_board[x][y+i+1] = 0
            possible_states.append(new_board)
        # move right
        if y == 2:
            new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
            for i in range(2):
                new_board[x][y-i] = new_board[x][y-i-1]
                new_board[x][y-i-1] = 0
            possible_states.append(new_board)
        return possible_states
    
    # pose d'un pion rond sur un carré inoccupé
    def posePion(self):
        player = self.current_player
        # if the player's pawns aren't all on the board, he can't pose a pawn
        if sum([row.count(player) for row in self.plateau]) == 3:
            return []
        possible_states = []
        for i in range(3):
            for j in range(3):
                if self.plateau[i][j] == -1: #if the case is empty
                    new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
                    new_board[i][j] = player
                    possible_states.append(new_board)
        return possible_states
    
    def poseSurCarreVideo(self, x, y, player):
        possible_states = []
        # print("x,y = {} {}".format(x, y))
        for i in range(3):
            for j in range(3):
                if self.plateau[i][j] == -1:
                    # print("plateau[{}][{}] = {}".format(i, j, self.plateau[i][j]))
                    new_board = [[self.plateau[i][j] for j in range(3)] for i in range(3)]
                    new_board[i][j] = player
                    new_board[x][y] = -1
                    possible_states.append(new_board)
        
        # print("{} poseSurCarreVide possible".format(len(possible_states)))
        # for move in possible_states:
        #     for mv in move:
        #         print(mv)
        #     print()
        return possible_states
    
    # déplacement d'un pion rond déjà en place vers n'importe quel carré libre
    def movePion(self):
        player = self.current_player
        possible_states = []
        for i in range(3):
            for j in range(3):
                if self.plateau[i][j] == player: #if the case is empty
                    possible_states += self.poseSurCarreVideo(i, j, player)
        return possible_states

    def move(self):
        return self.moveOneCase() + self.moveTwoCases() + self.posePion() + self.movePion()

if __name__ == "__main__":
    game = Force3()
    print(game.plateau)
    moves =  game.move()
    print("{} moves possible".format(len(moves)))
    for move in moves:
        for mv in move:
            print(mv)
        print()

    # print("moving the empty case")
    # game.plateau = [[-2, -1, 0], [-1, -1, -1], [-1, -1, 1]]
    # game.empty_case = (0, 2)
    # print(game.plateau)
    # moves =  game.move()
    # # print("moves {}".format(moves))
    # print("{} moves possible".format(len(moves)))
    # for move in moves:
    #     for mv in move:
    #         print(mv)
    #     print()

    # game = Force3()
    # test pose pion
    # game.plateau = [[-1, -1, 0], [2, -1, 1], [-1, -1, 1]]
    # game.current_player = 2
    # print(game.plateau)
    # states = game.posePion()
    # print("{} moves possible".format(len(states)))
    # for move in states:
    #     for mv in move:
    #         print(mv)
    #     print()

    # game.plateau = [[-1, -1, 0], [2, -1, 1], [-1, 2, 1]]
    # game.current_player = 2
    # print(game.plateau)
    # states = game.movePion()
    # print("{} poses possible".format(len(states)))
    # for move in states:
    #     for mv in move:
    #         print(mv)
    #     print()
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

    def getPlayerPawns(self):
        return [(i, j) for i in range(3) for j in range(3) if self.plateau[i][j] == self.current_player]

    def getOpponentPawns(self):
        return [(i, j) for i in range(3) for j in range(3) if self.plateau[i][j] != self.current_player and self.plateau[i][j] != -1 and self.plateau[i][j] != 0]
    
    """check if points that are in the list are all aligned
    
    Keyword arguments:
    l -- list of points
    Return: returns an integer if the points are aligned, otherwise, it return the number of points that are aligned
    """
    def f(self, l):
        if len(l) <= 1:
            return 0 # len(l)
        # they are aligned diagonaly if for each point A and B, the difference abs(XB-XA) == abs(YB-YA) 
        # they are aligned vertically if for each point A and B, XB == XA
        # they are aligned horizontally if for each point A and B, YB == YA
        # implement
        # Check if points are aligned diagonally
        # diagonal_aligned = [[list(l[i-1])] + [list(l[i])] for i in range(1, len(l)) if abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1])]#sum(abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1]) for i in range(1, len(l)))
        diagonal_aligned = [l[i-1:i+1] for i in range(1, len(l)) if abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1])]
        diagonal_aligned = []
        diagonal_aligned.extend([l[i-1], l[i]] for i in range(1, len(l)) if abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1]))
        diagonal_aligned = []
        for i in range(1, len(l)):
            if abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1]):
                aligned_points = [l[i-1], l[i]]
                diagonal_aligned.extend(aligned_points)

        # Check if points are aligned horizontally
        horizontal_aligned = [tuple(l[i-1:i+1]) for i in range(1, len(l)) if l[i][0] == l[i-1][0]] #sum(l[i][0] == l[i-1][0] for i in range(1, len(l)))
        horizontal_aligned = []
        for i in range(1, len(l)):
            if l[i][0] == l[i-1][0]:
                aligned_points = [l[i-1], l[i]]
                horizontal_aligned.extend(aligned_points)
        # Check if points are aligned vertically
        vertical_aligned = [tuple(l[i-1:i+1]) for i in range(1, len(l)) if l[i][1] == l[i-1][1]] #sum(l[i][1] == l[i-1][1] for i in range(1, len(l)))
        vertical_aligned = []
        for i in range(1, len(l)):
            if l[i][1] == l[i-1][1]:
                aligned_points = [l[i-1], l[i]]
                vertical_aligned.extend(aligned_points)

        diagonal_aligned = set(diagonal_aligned)
        vertical_aligned = set(vertical_aligned)
        horizontal_aligned = set(horizontal_aligned)

        print("diagonal_aligned {}".format(diagonal_aligned))
        print("vertical_aligned {}".format(vertical_aligned))
        print("horizontal_aligned {}".format(horizontal_aligned))

        if len(diagonal_aligned) == 3 or len(vertical_aligned) == 3 or len(horizontal_aligned) == 3:
            return 1
        
        empty_squares = [(i, j) for i in range(3) for j in range(3) if self.plateau[i][j] == -1]
        print("empty_squares {}".format(empty_squares))

        if len(diagonal_aligned) == 2 and any(el in [(0,0), (0,2), (2,0), (2,2)] for el in diagonal_aligned): # il faut qu'au moins un des deux points soit sur un bord
            # check if any empty square and  the elements in the diagnal list are aligned
            if any(all(abs(al[0] - sq[0]) == abs(al[1] - sq[1]) for al in diagonal_aligned) for sq in empty_squares):
                return 100
            else:
                return 50
        
        if len(vertical_aligned) == 2:
            # check if the empty case and  the elements in the vertical list are aligned
            if any(all(al[1] == sq[1] for al in vertical_aligned) for sq in empty_squares):
                return 100
            else:
                return 50
        
        if len(horizontal_aligned) == 2:
            # check if the empty case and  the elements in the horizontal list are aligned
            if any(all(al[0] == sq[0] for al in horizontal_aligned) for sq in empty_squares):
                return 100
            else:
                return 50
            
        return 0
    

    """
    Fonction d’évaluation 
    Si deux pions sont alignés, la fonction eval sera fonction de la facilité à faire aligner le 3ème pion avec les autres. On peut donc vérifier si aucun pion de l’adversaire n’est sur la droite passant par les 2 pions, auquel cas la probabilité serait moins importante. 
    Si aucun pion adversaire n’est sur la droite, la probabilité est alors très forte 
    """
    def eval(self):
        player = self.current_player
        pawns = self.getPlayerPawns()
        print("pawns {}".format(pawns))
        return self.f(pawns)

    

if __name__ == "__main__":
    game = Force3()
    game.plateau = [[-2, -1, 0], [-1, -1, -1], [-1, -1, 1]]
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

    game.plateau = [[1, -1, 0], 
                    [1, 2, 1], 
                    [-1, 2, 2]]
    game.current_player = 2
    for ln in game.plateau:
        print(ln)
    print(game.eval())

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
import time


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
    

    def getEmptyCase(self, state=None):
        """returns the empty case"""
        if state is None:
            state = self.plateau
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return None

    def moveOneCase(self, state=None, player=None):
        """
        Gets the empty case and return the possible states of the board if the current player moves one case
        """
        if state is None:
            state = self.plateau
        try:
            x, y = self.getEmptyCase(state)
            possible_states = []
            if player is None:
                player = self.current_player
            # clone the board
            # move up
            # print(x,y)
            if x <= 1 and x+1 <= 2:
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                new_board[x][y] = new_board[x+1][y]
                new_board[x+1][y] = 0
                possible_states.append(new_board)
            # move down
            if x <= 1 and x-1 >= 0:
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                new_board[x][y] = new_board[x-1][y]
                new_board[x-1][y] = 0
                possible_states.append(new_board)
            # move left
            if y <= 1: # and y+1 <= 2
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                new_board[x][y] = new_board[x][y+1]
                new_board[x][y+1] = 0
                possible_states.append(new_board)
            # move right
            if y >= 1 : #and y-1 >= 0
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                new_board[x][y] = new_board[x][y-1]
                new_board[x][y-1] = 0
                possible_states.append(new_board)
            return possible_states
        
        except Exception as e:
            # print("error {}".format(e))
            return []
        
        
    def moveTwoCases(self, state=None, player=None):
        
        if state is None:
            state = self.plateau
        if player is None:
            player = self.current_player
        try:
            x, y = self.getEmptyCase(state)
            possible_states = []
            # clone the board
            # move up
            if x == 0:
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                for i in range(2):
                    new_board[x+i][y] = new_board[x+i+1][y]
                    new_board[x+i+1][y] = 0
                possible_states.append(new_board)
            # move down
            if x == 2:
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                for i in range(2):
                    new_board[x-i][y] = new_board[x-i-1][y]
                    new_board[x-i-1][y] = 0
                possible_states.append(new_board)
            # move left
            if y == 0:
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                for i in range(2):
                    new_board[x][y+i] = new_board[x][y+i+1]
                    new_board[x][y+i+1] = 0
                possible_states.append(new_board)
            # move right
            if y == 2:
                new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                for i in range(2):
                    new_board[x][y-i] = new_board[x][y-i-1]
                    new_board[x][y-i-1] = 0
                possible_states.append(new_board)
            return possible_states
        
        except Exception as e:
            # print("error {}".format(e))
            return []
    
    # pose d'un pion rond sur un carré inoccupé
    def posePion(self, state=None, player=None):
        if state is None:
            state = self.plateau
        if player is None:
            player = self.current_player
        # if the player's pawns aren't all on the board, he can't pose a pawn
        if sum([row.count(player) for row in state]) == 3:
            return []
        possible_states = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == -1: #if the case is empty
                    new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                    new_board[i][j] = player
                    possible_states.append(new_board)
        return possible_states
    
    def poseSurCarreVideo(self, x, y, player, state=None):
        possible_states = []
        if state is None:
            state = self.plateau
        # print("x,y = {} {}".format(x, y))
        for i in range(3):
            for j in range(3):
                if state[i][j] == -1:
                    # print("plateau[{}][{}] = {}".format(i, j, self.plateau[i][j]))
                    new_board = [[state[i][j] for j in range(3)] for i in range(3)]
                    new_board[i][j] = player
                    new_board[x][y] = -1
                    possible_states.append(new_board)
        
        
        return possible_states
    
    # déplacement d'un pion rond déjà en place vers n'importe quel carré libre
    def movePion(self, state=None, player=None):
        if player is None:
            player = self.current_player
        if state is None:
            state = self.plateau
        possible_states = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == player: #if the case is empty
                    possible_states += self.poseSurCarreVideo(i, j, player)
        return possible_states

    def move(self, state=None, player=None):
        """returns the possible moves for the current player"""
        if state is None:
            print("state is None")
            state = self.plateau
        if player is None:
            player = self.current_player
        # print("move_plateau : {}".format(state))
        return self.posePion(state, player) + self.movePion(state, player) + self.moveOneCase(state=state, player=player) + self.moveTwoCases(state, player)

    def getPlayerPawns(self, position=None, player=None):
        """returns a list corresponding to the coordinates of a player's pawns"""
        if player is None and position is None:
            player = self.current_player
            position = self.plateau

        return [(i, j) for i in range(3) for j in range(3) if position[i][j] == player]

    def getOpponentPawns(self):
        return [(i, j) for i in range(3) for j in range(3) if self.plateau[i][j] != self.current_player and self.plateau[i][j] != -1 and self.plateau[i][j] != 0]
    
    """check if points that are in the list are all aligned
    
    Keyword arguments:
    l -- list of points
    Return: returns an integer if the points are aligned, otherwise, it return the number of points that are aligned
    """
    def f(self, l, plateau=None):
        """takes a list of points(of a player) and returns a number according to the number of points that are aligned"""
        res = len(l)
        if len(l) <= 1:
            # print("len(l) <= 1, l={}".format(l))
            return res#0 # len(l)
        if plateau is None:
            plateau = self.plateau
        # they are aligned diagonaly if for each point A and B, the difference abs(XB-XA) == abs(YB-YA) 
        # they are aligned vertically if for each point A and B, XB == XA
        # they are aligned horizontally if for each point A and B, YB == YA
        # implement
        # Check if points are aligned diagonally
        # diagonal_aligned = [[list(l[i-1])] + [list(l[i])] for i in range(1, len(l)) if abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1])]#sum(abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1]) for i in range(1, len(l)))
        # print("f_plateau : {}".format(plateau))
        diagonal_aligned = []
        for i in range(1, len(l)):
            if abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1]):
                aligned_points = [l[i-1], l[i]]
                diagonal_aligned.extend(aligned_points)

        # Check if points are aligned horizontally
        horizontal_aligned = []
        for i in range(1, len(l)):
            if l[i][0] == l[i-1][0]:
                aligned_points = [l[i-1], l[i]]
                horizontal_aligned.extend(aligned_points)
        # Check if points are aligned vertically
        vertical_aligned = []
        for i in range(1, len(l)):
            if l[i][1] == l[i-1][1]:
                aligned_points = [l[i-1], l[i]]
                vertical_aligned.extend(aligned_points)

        # print("diagonal_aligned {}".format(diagonal_aligned))
        # print("vertical_aligned {}".format(vertical_aligned))
        # print("horizontal_aligned {}".format(horizontal_aligned))
        diagonal_aligned = set(diagonal_aligned)
        vertical_aligned = set(vertical_aligned)
        horizontal_aligned = set(horizontal_aligned)


        if len(diagonal_aligned) == 3 or len(vertical_aligned) == 3 or len(horizontal_aligned) == 3:
            return 100 # 1+len(l)
        
        empty_squares = [(i, j) for i in range(3) for j in range(3) if plateau[i][j] == -1]
        # print("empty_squares {}".format(empty_squares))

        if len(diagonal_aligned) == 2 and any(el in [(0,0), (0,2), (2,0), (2,2)] for el in diagonal_aligned): # il faut qu'au moins un des deux points soit sur un bord
            # check if any empty square and  the elements in the diagnal list are aligned
            # print("diagonal_aligned {}".format(diagonal_aligned))
            if any(all(abs(al[0] - sq[0]) == abs(al[1] - sq[1]) for al in diagonal_aligned) for sq in empty_squares):
                # print("diagonal_aligned {} || empty_square={}".format(diagonal_aligned, empty_squares))
                # time.sleep(0.1)
                res += 0.9#+len(l)
            else:
                res += 0.5#+len(l)
        
        if len(vertical_aligned) == 2:
            # check if the empty case and  the elements in the vertical list are aligned
            if any(all(al[1] == sq[1] for al in vertical_aligned) for sq in empty_squares):
                res += 0.9#+len(l)
            else:
                res += 0.5#+len(l)
        
        if len(horizontal_aligned) == 2:
            # check if the empty case and  the elements in the horizontal list are aligned
            if any(all(al[0] == sq[0] for al in horizontal_aligned) for sq in empty_squares):
                res += 0.9#+len(l)
            else:
                res += 0.5#+len(l)
            
        return res 
    
     
    """
    Fonction d’évaluation 
    Si deux pions sont alignés, la fonction eval sera fonction de la facilité à faire aligner le 3ème pion avec les autres. On peut donc vérifier si aucun pion de l’adversaire n’est sur la droite passant par les 2 pions, auquel cas la probabilité serait moins importante. 
    Si aucun pion adversaire n’est sur la droite, la probabilité est alors très forte 
    """
    def eval(self, position=None, player=None):
        if player is None:
            player = self.current_player
        if position is None:
            print("position is None")
            position = self.plateau
        # print("eval_plateau : {}".format(position))
        pawns = self.getPlayerPawns(position,player)
        ennemi_pawns = self.getPlayerPawns(position, 3-player)
        # # print("pawns {}".format(pawns))
        point = self.f(pawns, position)
        ennemi_point = self.f(ennemi_pawns, position)
        return point - ennemi_point
        if player == 1:
            point = -point
        return point
    
    def isFinal(self, position=None):
        """Check if the game is over"""
        if position is None:
            position = self.plateau
        for player in range(1,3):
            # self.current_player = player
            l = self.getPlayerPawns(position=position, player=player)
            if len(l) <= 1:
                continue # len(l)
            diagonal_aligned = []
            for i in range(1, len(l)):
                if abs(l[i][0] - l[i-1][0]) == abs(l[i][1] - l[i-1][1]):
                    aligned_points = [l[i-1], l[i]]
                    diagonal_aligned.extend(aligned_points)

            horizontal_aligned = []
            for i in range(1, len(l)):
                if l[i][0] == l[i-1][0]:
                    aligned_points = [l[i-1], l[i]]
                    horizontal_aligned.extend(aligned_points)
            
            vertical_aligned = []
            for i in range(1, len(l)):
                if l[i][1] == l[i-1][1]:
                    aligned_points = [l[i-1], l[i]]
                    vertical_aligned.extend(aligned_points)

            diagonal_aligned = set(diagonal_aligned)
            vertical_aligned = set(vertical_aligned)
            horizontal_aligned = set(horizontal_aligned)

            if len(diagonal_aligned) == 3 or len(vertical_aligned) == 3 or len(horizontal_aligned) == 3:
                return True
        return False
        player = self.current_player
        pawns = self.getPlayerPawns()
        return self.f(pawns) == 1000

    

def minimax(game:Force3, position:list, maximizingPlayer:bool, depth=-1, alpha=-1000, beta=1000):
    
    """Implement the minimax algorithm"""
    player = 2 if maximizingPlayer else 1
    if game.isFinal(position) or depth == 0:
        return game.eval(position, player), position
    moves = game.move(position, player)
    
    # print("moves {}".format(moves))
    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        for pos in moves:
            # print("visiting node {}; pos={}".format(nodes_visited, pos))
            eval = minimax(game, pos, False, depth-1, alpha, beta)[0]
            # print("eval: {}, maxeval: {}".format(eval, maxEval))
            maxEval = max(maxEval, eval)
            if maxEval == eval:
                best_move = pos
        return maxEval, best_move
    else:
        minEval = float('inf')
        for pos in moves:
            # print("visiting node {}".format(nodes_visited))
            eval = minimax(game, pos, True, depth-1, alpha, beta)[0]
            # print("eval: {}, mineval: {}".format(eval, minEval))
            minEval = min(minEval, eval)
            if minEval == eval:
                best_move = pos
        return minEval, best_move
    

if __name__ == "__main__":
    game = Force3()
    print(game.isFinal([[1, -1, 2], [-1, -1, 2], [0, 1, 2]]))
    game.plateau = [[1, -1, -1],
                [2, 0, -1],
                [-1, 1, 2]]
   
    depth =4
    plateau = [[1, -1, -1],
                [2, 0, -1],
                [-1, 1, 2]]
    for i in range(0,100):
        start = time.time()
        maximizing = True if i%2 == 0 else False
        minmax_return = minimax(game, plateau, maximizingPlayer=maximizing, depth=depth)
        plateau = minmax_return[1]
        # print(minmax_return)
        end = time.time()
        print("player: {}, point={} time={}".format(2 if maximizing else 1, minmax_return[0],end-start))
        for mv in minmax_return[1]:
            print('\t',mv)
   
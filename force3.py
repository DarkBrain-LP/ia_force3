from datetime import time
import time as tm
import flet as ft
from copy import deepcopy
from model import Force3, minimax

CARD_WIDTH = 70
CARD_HEIGTH = 100
CARD_OFFSET = 20


class Card(ft.GestureDetector):

    def __init__(self, game, slot=None, color=None, border_radius=0, height=CARD_HEIGTH, width=CARD_WIDTH):
        super().__init__()
        self.slot = slot
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.left = None
        self.top = None
        # self.pawn = None
        self.game = game
        self.color = color
        self.content = ft.Container(bgcolor=self.color, width=width, height=height,
                                    border_radius=border_radius)

    def move_on_top(self):
        """Moves draggable card to the top of the stack"""
        for item in self.get_draggable_items():
            self.game.controls.remove(item)
            self.game.controls.append(item)
            self.game.update()
        # self.game.controls.remove(self)
        # self.game.controls.append(self)
        # self.game.remove(self)
        # self.game.append(self)
        try:
            self.game.update()
        except:
            pass

    def bounce_back(self):
        """Returns card to its original position"""
        try:
            draggable_items = self.get_draggable_items()
            for item in draggable_items:
                item.top = self.game.start_top + draggable_items.index(item) * CARD_OFFSET
                item.left = self.game.start_left
                board = [[-1, 2, 2], [-1, 0, -1], [-1, 1, 1]]
                # self.game.place_pawns_from_board(board)
            # if type(self) == Card:
            #     self.top = self.slot.top
            #     self.left = self.slot.left
            # else:
            #     if self.slot is not None:
            #         self.top = self.game.start_top
            #         self.left = self.game.start_left
        except:
            self.top = self.top
            self.left = self.left
        # try:
        self.game.update()
        # self.update()

    def place(self, slot):
        """Place card to the slot"""
        draggable_items = self.get_draggable_items()
        # TODO : check if it is a two move action. If it is then move the pawns on the line
        try:
            
            # check if we can move two slots contents from left to right
            if not self.game.initiating and slot.left == 0 and self.game.start_left == 200 and slot.top == self.slot.top:
                # swap the slots
                print("===> right to left")
                print(self.game.nb_moves_after_two_moves)
                if not self.game.can_make_hor_two_moves:
                    self.bounce_back()
                    return

                draggables = self.get_draggable_items()
                for el in draggables:
                    el.left = self.game.start_left - 100
                    el.top = slot.top + draggables.index(el) * CARD_OFFSET
                    self.game.update()
                self.slot.left = self.game.start_left - 100  # mettre a jour le 100 en même temps ???
                self.game.update()
                slot.left = self.game.start_left
                slot.update()
                "The following commented code's purpose was to reset the middle slot's pile elements to their correct " \
                "top position"
                # if slot.pile is not None and len(slot.pile) != 0:
                #     slot_draggables = slot.pile[0].get_draggable_items()
                #     i = 0
                #     for el in slot_draggables:
                #         el.left = self.game.start_left
                #         el.top = slot.top + i * CARD_OFFSET  # slot_draggables.index(el) * CARD_OFFSET
                #         i += 1
                #         self.game.update()
                #         # el.update()
                slot_els = slot.pile
                for el in slot_els:
                    el.left = self.game.start_left
                    el.top = slot.top + slot_els.index(el) * CARD_OFFSET
                # el.update()
                self.game.update()
                # self.game.update()
                # get the horizontal slots
                self.game.start_top = slot.top
                horiz_slots = self.game.get_horizontal_slots()
                # sort by left
                horiz_slots.sort(key=lambda x: x.left, reverse=True)
                horiz_slots = horiz_slots[1]
                horiz_slots.left = 0
                horiz_slots.update()
                middle_items = horiz_slots.pile
                for el in middle_items:
                    el.left = 0

                reset_slots = self.game.get_horizontal_slots()
                reset_slots[0] = horiz_slots
                index = 3 * (-1 + self.game.start_top // 110)
                self.game.slots[index] = horiz_slots
                reset_slots[1] = self.slot
                self.game.slots[index + 1] = self.slot
                reset_slots[2] = slot
                self.game.slots[index + 2] = slot

                self.game.update()
                # update the two moves counter
                self.game.nb_moves_after_two_moves = 1
                self.game.can_make_hor_two_moves = False
                self.game.can_make_vert_two_moves = True

                return

            # check if we can move two slots contents from right to left
            if not self.game.initiating and slot.left == 200 and self.game.start_left == 0 and slot.top == self.slot.top:
                print("===> left to right")
                print(self.game.nb_moves_after_two_moves)
                if not self.game.can_make_hor_two_moves:
                    self.bounce_back()
                    return

                draggables = self.get_draggable_items()
                for el in draggables:
                    el.left = self.game.start_left + 100
                    # TODO : place thee elements at the right top position
                    el.top = slot.top
                    self.game.update()
                self.slot.left = self.game.start_left + 100  # mettre a jour le 100 en même temps ???
                self.game.update()
                slot.left = self.game.start_left
                # slot.update()
                slot_els = slot.pile
                for el in slot_els:
                    el.left = self.game.start_left
                    # el.update()
                self.game.update()
                # self.game.update()
                # get the horizontal slots
                horiz_slots = self.game.get_horizontal_slots()
                # sort by left
                horiz_slots.sort(key=lambda x: x.left, reverse=True)
                horiz_slots = horiz_slots[1]
                horiz_slots.left = 200
                horiz_slots.update()
                middle_items = horiz_slots.pile
                for el in middle_items:
                    el.left = 200

                reset_slots = self.game.get_horizontal_slots()
                reset_slots[0] = horiz_slots
                index = 3 * (-1 + self.game.start_top // 110)
                self.game.slots[index] = slot
                reset_slots[1] = self.slot
                self.game.slots[index + 1] = self.slot
                reset_slots[2] = slot
                self.game.slots[index + 2] = horiz_slots

                self.game.update()
                # update the two moves counter
                self.game.nb_moves_after_two_moves = 1
                self.game.can_make_hor_two_moves = False
                self.game.can_make_vert_two_moves = True
                return

            # check if we can move two slots contents from up to down
            if not self.game.initiating and slot.top == 330 and self.game.start_top == 110 and slot.left == self.slot.left:
                print("===> up to down")
                print(self.game.nb_moves_after_two_moves)
                if not self.game.can_make_vert_two_moves:
                    self.bounce_back()
                    return

                draggables = self.get_draggable_items()
                for el in draggables:
                    el.top = self.game.start_top + 110
                    # TODO : place thee elements at the right top position
                    el.left = slot.left
                    self.game.update()
                self.slot.top = self.game.start_top + 110
                self.game.update()
                slot.top = self.game.start_top
                # slot.update()
                slot_els = slot.pile
                for el in slot_els:
                    el.top = self.game.start_top
                    # el.update()
                self.game.update()
                # self.game.update()
                # get the horizontal slots
                vert_slots = self.game.get_vertical_slots()
                # sort by left
                vert_slots.sort(key=lambda x: x.top, reverse=True)
                vert_slots = vert_slots[1]
                vert_slots.top = 330
                vert_slots.update()
                middle_items = vert_slots.pile
                for el in middle_items:
                    el.top = 330
                reset_slots = self.game.get_vertical_slots()
                reset_slots[0] = vert_slots
                index = self.game.start_left // 100
                self.game.slots[index] = slot
                reset_slots[1] = self.slot
                self.game.slots[index + 3] = self.slot
                reset_slots[2] = slot
                self.game.slots[index + 6] = vert_slots

                self.game.update()
                # update the two moves counter
                self.game.nb_moves_after_two_moves = 1
                self.game.can_make_vert_two_moves = False
                self.game.can_make_hor_two_moves = True
                return

            # check if we can move two slots contents from down to up
            if not self.game.initiating  and slot.top == 110 and self.game.start_top == 330 and slot.left == self.slot.left:
                print("===> down to up")
                print(self.game.nb_moves_after_two_moves)
                if not self.game.can_make_vert_two_moves:
                    self.bounce_back()
                    return
                draggables = self.get_draggable_items()
                for el in draggables:
                    el.top = self.game.start_top - 110
                    # TODO : place thee elements at the right top position
                    el.left = slot.left
                    self.game.update()
                self.slot.top = self.game.start_top - 110
                self.game.update()
                slot.top = self.game.start_top
                # slot.update()
                slot_els = slot.pile
                for el in slot_els:
                    el.top = self.game.start_top
                    # el.update()
                self.game.update()
                # self.game.update()
                # get the horizontal slots
                vert_slots = self.game.get_vertical_slots()
                # sort by left
                vert_slots.sort(key=lambda x: x.top, reverse=True)
                vert_slots = vert_slots[1]
                vert_slots.top = 110
                vert_slots.update()
                middle_items = vert_slots.pile
                for el in middle_items:
                    el.top = 110
                reset_slots = self.game.get_vertical_slots()
                reset_slots[0] = vert_slots
                index = self.game.start_left // 100
                self.game.slots[index] = vert_slots
                reset_slots[1] = self.slot
                self.game.slots[index + 3] = self.slot
                reset_slots[2] = slot
                self.game.slots[index + 6] = slot

                self.game.update()
                # update the two moves counter
                self.game.nb_moves_after_two_moves = 1
                self.game.can_make_vert_two_moves = False
                self.game.can_make_hor_two_moves = True
                return
            
            # One move handler
            for item in draggable_items:
                item.top = slot.top + draggable_items.index(item) * CARD_OFFSET
                item.left = slot.left
                if item.slot is not None:
                    item.slot.pile.remove(item)
                item.slot = slot
                slot.pile.append(item)
                # update the two moves counter
                self.game.nb_moves_after_two_moves = 0
                self.game.can_make_hor_two_moves = True
                self.game.can_make_vert_two_moves = True

        except Exception as e:
            pass

    def start_drag(self, e: ft.DragStartEvent):
        # TODO : add the slot pile to the game instance to remove the card/pawn from it after drop is completed
        # disable the drag if it is not the current player's turn
        # if not self.game.is_current_player_pawn(self):
        #     self.bounce_back()
        #     return
        
        self.game.start_top = e.control.top
        self.game.start_left = e.control.left
        self.move_on_top()
        # self.update()
        self.game.update()

    def drag(self, e: ft.DragUpdateEvent):
        if not self.game.is_current_player_pawn(self):
            self.bounce_back()
            return
        draggable_items = self.get_draggable_items()
        for item in draggable_items:
            # print("offset = {}".format(draggable_items.index(item) * CARD_OFFSET))
            item.top = max(0, item.top + e.delta_y)  # + draggable_items.index(item) * CARD_OFFSET
            item.left = max(0, item.left + e.delta_x)
            self.game.update()
        # self.top = max(0, self.top + e.delta_y)
        # self.left = max(0, self.left + e.delta_x)
        # self.update()
        self.game.update()

    def drop(self, e: ft.DragEndEvent):
        for slot in self.game.slots:
            if (
                    abs(self.top - slot.top) < 20
                    and abs(e.control.left - slot.left) < 20
            ):
                if slot.can_place(self):
                    self.place(slot)
                else:
                    self.bounce_back()
                # self.update()
                self.game.update()
                print("board = {}".format(self.game.convert_game_to_force3_board()))
                board = [[-1, 2, 2], [-1, 0, -1], [-1, 1, 1]]
                # self.game.draw_board(board)
                # print("board = {}".format(self.game.convert_game_to_force3_board()))
                # print("is_game_over = {}".format(self.game.is_game_over()))
                if self.game.is_game_over():
                    # TODO : show dialog with winner
                    # print("The winner is : {}".format(self.game.ai_model.get_winner(self.game.convert_game_to_force3_board())))
                    self.game.show_game_over_dialog()
                
                self.game.current_player = 3 - self.game.current_player
                print("next_player = {}".format(self.game.current_player))
                # if it is the AI's turn, then play
                if self.game.current_player == 2:
                    # TODO : call the AI method to play
                    # call model to play
                    # delete the controls
                    # make a deepcopy of the game
                    state = self.game.convert_game_to_force3_board()
                    board = minimax(self.game.ai_model, state, True, depth=5)[1]
                    new_game = Game(plateau=board,page=self.game.page, vert_moves=self.game.can_make_vert_two_moves, hor_moves=self.game.can_make_hor_two_moves, current_player=self.game.current_player)
                    self.game.page.controls.remove(self.game)
                    self.game.page.update()
                    # deep_copy = deepcopy(self.game)
                    new_game.page.add(new_game)
                    # self.game.page.update()
                    new_game.page.update()
                    #check if the game is over
                    if new_game.is_game_over():
                        # TODO : show dialog with winner
                        # print("The winner is : {}".format(self.game.ai_model.get_winner(self.game.convert_game_to_force3_board())))
                        new_game.show_game_over_dialog()


                    self.game.delete_controls()
                    del self.game
                    # self.game.ai_play()
                    # self.game.page.add(self.game)
                return
        self.bounce_back()
        # print board
        # self.update()
        self.game.update()

    def get_draggable_items(self) -> list:
        """returns the card with the pawn on it"""
        try:
            return self.slot.pile[self.slot.pile.index(self):] if self.slot is not None else [self]
        except:
            return [self]
        if self.slot is not None:
            return self.slot.pile[-1]


class Pawn(Card):
    def __init__(self, game, card: Card, top, left, color, border_radius=50, height=CARD_HEIGTH / 2, width=CARD_WIDTH):
        super().__init__(game=game, color=color, border_radius=border_radius, height=height, width=width)
        self.top = top
        self.left = left

    # place the pawn
    def place(self, slot):
        """Place pawn to the card"""
        # # TODO : check if it is a two move action. If it is then move the pawns on the line
        # if ((abs(self.slot.top - slot.top) == 220) and abs(self.slot.left - slot.left) == 0) or (((slot.left == 0) or (slot.left == 200)) and slot.top == self.slot.top):
        #     print("place card : It is a two move !!!")
        self.top = slot.top + len(slot.pile) * CARD_OFFSET  # / 2
        self.left = slot.left  # / 2
        if self.slot is not None and len(self.slot.pile) != 0:
            self.slot.pile.remove(self)
        self.slot = slot
        slot.pile.append(self)
        
        # update the two moves counter
        self.game.nb_moves_after_two_moves = 0
        self.game.can_make_hor_two_moves = True
        self.game.can_make_vert_two_moves = True
        # print("after_place_pawn", "dest_slot_pile={}, pawn_slot_pile={}".format(slot.pile, self.slot.pile))
        if not self.game.initiating:
            slot.update()
            # self.update()
            self.game.update()

    # place the pawn
    def init(self, slot):
        """Place pawn to the card"""
        self.top = slot.top  # / 2
        self.left = slot.left  # / 2
        self.slot = slot
        self.slot.pile.append(self)


class Game(ft.Stack):
    def __init__(self, plateau=None, page=None, vert_moves=False, hor_moves=False, current_player=1):
        super().__init__()
        self.slots = []
        self.game_cards = []
        self.pawn_slot1 = []
        self.pawn_slot2 = []
        self.pawn1_cards = []
        self.pawn2_cards = []
        self.controls = []
        self.start_top = 0
        self.start_left = 0
        self.current_pile = []
        self.width = 1000
        self.height = 1000
        self.initiating = True
        self.current_player = current_player
        self.nb_moves_after_two_moves = 0
        self.can_make_hor_two_moves = hor_moves
        self.can_make_vert_two_moves = vert_moves
        self.ai_model = Force3()# [[1, -1, -1],
                                #         [-1, -1, -1],
                                #         [0, -1, 2]]
        self.create_cards(plateau) # self.ai_model.plateau
        self.page = page

    def ai_play(self):
        self.ai_model.current_player = 2
        self.ai_model.plateau = self.convert_game_to_force3_board()
        board = minimax(self.ai_model, self.ai_model.plateau, True, depth=3)[1]
        self.ai_model.plateau = board
        self.create_cards(board, self.can_make_vert_two_moves, self.can_make_hor_two_moves, 1)
        self.update()
    # method that return to get if the pawn that is trying to be moved is for the current player
    def is_current_player_pawn(self, card: Card) -> bool:
        """Returns True if the pawn that is trying to be moved is for the current player"""
        if card.color == ft.colors.BROWN:
            return True
        if self.current_player == 1:
            return card.color == ft.colors.BLUE
        else:
            return card.color == ft.colors.RED

    def delete_controls(self):
        """Deletes the controls of the game"""
        for control in self.controls:
            self.controls.remove(control)
        self.controls = []
        # self.screen.fill((0, 0, 0))

    def create_cards(self, board: list[list[int]]=None, vert_moves=False, hor_moves=False, current_player=1):
        # create 9 slots
        self.initiating = True
        self.current_player = current_player
        self.nb_moves_after_two_moves = 0
        self.can_make_hor_two_moves = hor_moves
        self.can_make_vert_two_moves = vert_moves
        print("create_cards", "board={}".format(board))
        # print("create_cards", "controls={}".format(self.controls))
        # on supprime les éléments de l'interface si une configuration de plateau a été fournie
        # if board is not None:
        if self.controls != []:
            self.update()
            self.controls = []

        # let's create the slots that will contain the cards
        self.slots = []
        delta_x = 110
        for i in range(3):
            for j in range(3):
                self.slots.append(Slot(self, top=delta_x, left=100 * j))
            delta_x += 110

        # create 3 slots for pawn1 (no need)
        for i in range(3):
            self.pawn_slot1.append(Slot(self, top=0, left=100 * i))
            self.pawn_slot2.append(Slot(self, top=500, left=100 * i))
        # create 9 cards
        for i in range(9):
            self.game_cards.append(Card(self, color=ft.colors.BROWN))
            # self.controls.append(Card(self, ft.colors.BROWN))
        # create 3 cards for pawn1
        for i in range(3):
            self.pawn1_cards.append(Pawn(self, None, 0, 100 * i, ft.colors.RED))
            self.pawn2_cards.append(Pawn(self, None, 500, 100 * i, ft.colors.BLUE))
            # self.controls.append(Card(self, ft.colors.BLUE, border_radius=50))
        

        # cards drawing
        if board is None:
            for i in range(9):
                print("bug")
                if i == 4:
                    continue
                self.game_cards[i].place(self.slots[i])
                # print("create_cards", "pile={}".format(self.slots[i].pile))
        else:
            for i in range(3):
                for j in range(3):
                    pos = 3*i + j
                    if board[i][j] == 0: # si l'élément est vide, on ne pose pas de carré
                        print("create_cards", "empty={}".format(pos))
                        continue
                    self.game_cards[pos].place(self.slots[pos])
        
        # now we will place the pawns according to the board
        # place the pawns that are not on the board to their initial position
        if board is None:
            for i in range(3):
                self.pawn1_cards[i].init(self.pawn_slot1[i])
                self.pawn2_cards[i].init(self.pawn_slot2[i])
        else:
            played_red_pawns = [item for sublist in board for item in sublist if item == 2]
            played_blue_pawns = [item for sublist in board for item in sublist if item == 1]
            non_played_red_pawns = 3-len(played_red_pawns)
            non_played_blue_pawns = 3-len(played_blue_pawns)
            pawn1_index = 2
            pawn2_index = 2
            for i in range(non_played_red_pawns):
                self.pawn1_cards[pawn1_index].init(self.pawn_slot1[pawn1_index])
                pawn1_index -= 1
                played_red_pawns.append(2)
            for i in range(non_played_blue_pawns): # here, non_played_blue_pawns-1 items will be initialized
                self.pawn2_cards[pawn2_index].init(self.pawn_slot2[pawn2_index])
                pawn2_index -= 1
                played_blue_pawns.append(1)

            # now place the pawns that are on the board
            for i in range(3):
                for j in range(3):
                    value = board[i][j]
                    if value == 1:
                        self.pawn2_cards[pawn2_index].init(self.slots[i * 3 + j])
                        non_played_blue_pawns += 1
                        pawn2_index -= 1
                    elif value == 2:
                        self.pawn1_cards[pawn1_index].init(self.slots[i * 3 + j])
                        non_played_red_pawns += 1
                        pawn1_index -= 1

        self.controls.extend(self.slots)
        self.controls.extend(self.game_cards)
        self.controls.extend(self.pawn_slot1)
        self.controls.extend(self.pawn_slot2)
        self.controls.extend(self.pawn1_cards)
        self.controls.extend(self.pawn2_cards)

        self.initiating = False
 # method that returns the slots of the current horizontal line according to the start_top attribute
    def get_horizontal_slots(self) -> list:
        """Returns the slots of the current horizontal line according to the start_top attribute"""
        a = [slt for slt in self.slots if slt.top == self.start_top]
        return a

    # method that returns the slots of the current vertical line according to the start_left attribute

    def get_vertical_slots(self) -> list:
        """Returns the slots of the current vertical line according to the start_left attribute"""
        return [slt for slt in self.slots if slt.left == self.start_left]

    def redraw_cards(self, board: list[list[int]]):
        # create 9 slots
        # delete controls of the game
        for control in self.controls:
            self.remove(control)
        
        self.slots = []
        delta_x = 110
        for i in range(3):
            for j in range(3):
                self.slots.append(Slot(self, top=delta_x, left=100 * j))
            delta_x += 110

        # create 3 slots for pawn1 (no need)
        for i in range(3):
            self.pawn_slot1.append(Slot(self, top=0, left=100 * i))
            self.pawn_slot2.append(Slot(self, top=500, left=100 * i))
        # create 9 cards
        for i in range(9):
            self.game_cards.append(Card(self, color=ft.colors.BROWN))
            # self.controls.append(Card(self, ft.colors.BROWN))
        # create 3 cards for pawn1
        for i in range(3):
            self.pawn1_cards.append(Pawn(self, None, 0, 100 * i, ft.colors.RED))
            self.pawn2_cards.append(Pawn(self, None, 500, 100 * i, ft.colors.BLUE))
            # self.controls.append(Card(self, ft.colors.BLUE, border_radius=50))

        # cards initialization
        for i in range(3):
            for j in range(3):
                pos = 3*i + j
                if board[i][j] == 0: # si l'élément est vide, on ne pose pas de carré
                    continue
                self.game_cards[pos].place(self.slots[pos])
            # print("create_cards", "pile={}".format(self.slots[i].pile))

        # now we will place the items according to the board
        # place the pawns that are not on the board to their initial position
        played_red_pawns = [item for sublist in board for item in sublist if item == 2]
        played_blue_pawns = [item for sublist in board for item in sublist if item == 1]
        non_played_red_pawns = 3-len(played_red_pawns)
        non_played_blue_pawns = 3-len(played_blue_pawns)
        for i in range(non_played_red_pawns):
            self.pawn1_cards[i].init(self.pawn_slot1[i])
            played_red_pawns.append(2)
        for i in range(non_played_blue_pawns): # here, non_played_blue_pawns-1 items will be initialized
            self.pawn2_cards[i].init(self.pawn_slot2[i])
            played_blue_pawns.append(1)
        # for i in range(3):
        #     self.pawn1_cards[i].init(self.pawn_slot1[i])
        #     self.pawn2_cards[i].init(self.pawn_slot2[i])
            
        for i in range(3):
            for j in range(3):
                value = board[i][j]
                if value == 1:
                    self.pawn2_cards[non_played_blue_pawns+1].place(self.slots[i * 3 + j])
                    non_played_blue_pawns += 1
                elif value == 2:
                    self.pawn1_cards[non_played_red_pawns+1].place(self.slots[i * 3 + j])
                    non_played_red_pawns += 1


        self.controls.extend(self.slots)
        self.controls.extend(self.game_cards)
        self.controls.extend(self.pawn_slot1)
        self.controls.extend(self.pawn_slot2)
        self.controls.extend(self.pawn1_cards)
        self.controls.extend(self.pawn2_cards)
        self.initiating = False


    def convert_game_to_force3_board(self) -> list[list[int]]:
        board = [[0,0,0],
                 [0,0,0],
                 [0,0,0]]

        for i in range(3):
            for j in range(3):
                slot = self.slots[i * 3 + j]
                board[i][j] = 0  # Represent an empty slot
                if slot.pile:
                    top_item = slot.pile[-1]
                    if isinstance(top_item, Card) and top_item.color == ft.colors.BROWN:
                        board[i][j] = -1  # Represent a card
                    elif isinstance(top_item, Pawn):
                        if top_item.color == ft.colors.RED:
                            board[i][j] = 2
                        else :
                            board[i][j] = 1  # Represent a pawn

        return board

    def is_game_over(self) -> bool:
        """Returns True if the game is over"""
        board = self.convert_game_to_force3_board()
        print("is_game_over", "board={}".format(board))
        return self.ai_model.isFinal(board)
    
    def show_game_over_dialog(self):
        """Shows a dialog when the game is over"""
        tm.sleep(3)
        new_game = Game(page=self.page)
        self.page.controls.remove(self)
        self.page.update()
        # deep_copy = deepcopy(self.game)
        new_game.page.add(new_game)
        # self.game.page.update()
        new_game.page.update()
                    
        # self.create_cards()
        return
        if self.is_game_over():
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("GAME OVER"),
                content=ft.Text("Do you want to play again?"),
                actions=[
                    ft.TextButton("Yes", on_click=self.close_dlg),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )
            self.dialog = dlg
            self.page.add(dlg)
            dlg.open = True
            # self.controls.append(dlg)
            self.update()
    def close_dlg(self,e):
        self.dialog.open = False
        self.page.controls.remove(self.dialog)
        self.page.update()
        # self.controls.remove(self.dialog)
        self.update()
        self.create_cards()
        self.update()

    def reset_game(self):
        """Resets the game"""
        self.create_cards()

    
class Slot(ft.Container):
    def __init__(self, game, top, left, width=CARD_WIDTH, height=CARD_HEIGTH):
        super().__init__(top=top, left=left, width=width, height=height, border=ft.border.all(1))
        self.top = top
        self.left = left
        self.game = game
        self.card = None
        self.pile = []
        # self.border = ft.border.all(1)
        # self.content = ft.Container(bgcolor=color, width=CARD_WIDTH, height=CARD_HEIGTH)

    def place(self, card: Card):
        """Place card to the slot"""
        card.top = self.top
        card.left = self.left
        card.slot = self

    # method to swap two slots with all their content
    def swap(self, slot):
        """Swap two slots with all their content"""
        # swap the slots
        self.top, slot.top = slot.top, self.top
        self.left, slot.left = slot.left, self.left
        # swap the slots' piles
        # self.pile, slot.pile = slot.pile, self.pile
        # swap the slots' cards
        for i in range(len(self.pile)):
            # if type(self.pile[i]) == Pawn:
            #     self.pile[i].top = self.top
            # else:
            #     self.pile[i].top = self.top + i * CARD_OFFSET
            self.pile[i].top = self.top + i * CARD_OFFSET
            self.pile[i].left = self.left
        for i in range(len(slot.pile)):
            slot.pile[i].top = slot.top
            slot.pile[i].left = slot.left
            # slot.pile[i].slot = slot
        # update the slots
        self.update()
        slot.update()

    def can_place(self, child: Card | Pawn):
        """Check if card can be placed on the slot"""
        # print("can_place", "pile={}".format(self.pile))
        if isinstance(child, Pawn):
            return len(self.pile) == 1
        # case empty slot TODO : implement position consideration later
        print("self.top={}, self.left={}, child.slot.top={}, child.slot.left={}".format(self.top, self.left,
                                                                                        child.slot.top,
                                                                                        child.slot.left))
        if len(self.pile) == 0:
            # if ((self.top == CARD_HEIGTH + 10) or (self.top == 3*(CARD_HEIGTH + 10)) and abs(child.slot.left - self.left) == 0) or (((self.left == 0) or (self.left == 200)) and self.top == child.slot.top):
            if ((abs(child.slot.top - self.top) == 220) and abs(child.slot.left - self.left) == 0) or (
                    ((self.left == 0) or (self.left == 200)) and self.top == child.slot.top):
                print("can_place 2 : True")
                return True
            return (abs(child.slot.left - self.left) == 100 and abs(child.slot.top - self.top) == 0) or (
                    abs(child.slot.left - self.left) == 0 and abs(child.slot.top - self.top) == 110)


# flet main
def main(page: ft.Page):
    force3 = Game(page=page)
    
    
    page.add(force3)
    # btn1 = ft.ElevatedButton(text="Elevated button"),
    # btn2 = ft.ElevatedButton("Disabled button", disabled=True),
    
    # # add the force3 game and the buttons to the a column
    # page.add(ft.Column(
    #     controls=[
    #         force3,
    #         btn1,
    #         btn2
    #     ]
    # ))
    # page.add(dlg_modal)
    page.update()


    # def open_dlg_modal(e):
    #     page.dialog = dlg_modal
    #     dlg_modal.open = True
    #     page.update()

    # def close_dlg(e):
    #     dlg_modal.open = False
    #     page.update()
    # dlg_modal = ft.AlertDialog(
    #     modal=True,
    #     title=ft.Text("Please confirm"),
    #     content=ft.Text("Do you really want to delete all those files?"),
    #     actions=[
    #         ft.TextButton("Yes", on_click=close_dlg),
    #         ft.TextButton("No", on_click=close_dlg),
    #     ],
    #     actions_alignment=ft.MainAxisAlignment.END,
    #     on_dismiss=lambda e: print("Modal dialog dismissed!"),
    # )


    
    # tm.sleep(2)
    # # delete the force3 game
    # page.controls.remove(force3)
    # page.update()

    # tm.sleep(2)
    # page.add(force3)
    # page.update()
    


ft.app(name="Force3", target=main)

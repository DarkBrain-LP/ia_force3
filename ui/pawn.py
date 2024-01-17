from datetime import time
import time as tm
import flet as ft
from copy import deepcopy
from card import Card
from model import Force3, minimax

CARD_WIDTH = 70
CARD_HEIGTH = 100
CARD_OFFSET = 20



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

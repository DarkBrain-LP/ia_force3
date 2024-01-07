import flet as ft
from card import Card
from pawn import Pawn

CARD_WIDTH = 70
CARD_HEIGTH = 100
CARD_OFFSET = 20



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


from datetime import time

import flet as ft

CARD_WIDTH = 70
CARD_HEIGTH = 100
CARD_OFFSET = 20


class Card(ft.GestureDetector):

    def __init__(self, game, slot=None, color=None, border_radius=0):
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
        self.content = ft.Container(bgcolor=self.color, width=CARD_WIDTH, height=CARD_HEIGTH,
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
            # if not self.game.initiating and slot.left == 0 and slot.top == self.slot.top:
            #     print("place card : It is a two horizontal right to left move !!!")
            #     # get the horizontal items
            # elif not self.game.initiating and slot.left == 200 and slot.top == self.slot.top:
            #     print("place card : It is a two horizontal left to right move !!!")
            #     # get the horizontal slots
            #     horiz_slots = [slt for slt in self.game.slots if slt.top == self.slot.top and slt.left != 200]
            #     # horiz_slots.sort(key=lambda x: x.left, reverse=True)
            #     for card_slot in self.game.slots:
            #         if card_slot.top == self.slot.top and card_slot.left != 200:
            #             # foreach slot, move the cards(with its pawn) to the right
            #             slot_contents = card_slot.pile
            #             for slot_item in slot_contents:
            #                 if type(slot_item) == Card:
            #                     draggable_items1 = slot_item.get_draggable_items()  # gets the slot items(card + pawn)
            #                     for el in draggable_items1:
            #                         # el.top = slot.top + draggable_items.index(el) * CARD_OFFSET
            #                         if (self.game.start_left - el.left) % 100 != 0: # supposing that the user cannot exactly place the card in position 0, 100 or 200 (0.xx, 100.xx, 200.xx instead)
            #                             el.left = self.game.start_left - 100
            #                         else:
            #                             el.left = el.left + 100  # move them to the right
            #                         self.game.controls.remove(el)
            #                         self.game.controls.append(el)
            #                         self.game.update()
            #                         # if el.slot is not None:
            #                         #     el.slot.pile.remove(el)
            #                         # el.slot = slot
            #                         # slot.pile.append(el)
            #             # break
            #     # if ((slot.left == 0) or (slot.left == 200)) and slot.top == self.slot.top:
            #     #     print("place card : It is a two horizontal move !!!")
            #     # get the horizontal items
            #     horizontal_items = []
            #
            # elif not self.game.initiating and self.slot.top - slot.top == 220 and abs(self.slot.left - slot.left) == 0:
            #     print("place card : It is a two vertical down to up move !!!")
            # elif not self.game.initiating and self.slot.top - slot.top == -220 and abs(self.slot.left - slot.left) == 0:
            #     print("place card : It is a two vertical up to down move !!!")
            # else:
            # check if we can move two slots contents from left to right
            if not self.game.initiating and slot.left == 0 and slot.top == self.slot.top:
                # swap the slots
                print("===> swap the slots")
                # putain = self.game.get_horizontal_slots()
                # putain[0], putain[1] = putain[1], putain[0]
                # putain[1], putain[2] = putain[2], putain[1]
                # self.game.update()
                # return
                draggables = self.get_draggable_items()
                for el in draggables:
                    el.left = self.game.start_left - 100  # slot.left
                    # el.top = slot.top + draggables.index(el) * CARD_OFFSET
                    # if type(el) == Card:
                    #     el.update()
                    self.game.update()
                self.slot.left = self.game.start_left - 100 # mettre a jour le 100 en même temps ???
                self.game.update()
                slot.left = self.game.start_left
                slot.update()
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
                horiz_slots.left = 0
                horiz_slots.update()
                middle_items = horiz_slots.pile
                for el in middle_items:
                    el.left = 0

                reset_slots = self.game.get_horizontal_slots()
                reset_slots[0] = horiz_slots
                self.game.slots[3] = horiz_slots
                reset_slots[1] = self.slot
                self.game.slots[4] = self.slot
                reset_slots[2] = slot
                self.game.slots[5] = slot

                # for i in range(len(horiz_slots)-1):
                #     horiz_slots[i].swap(horiz_slots[i + 2])
                #     # wait for 2 seconds don't use fl.sleep in the main thread
                #     # ft.sleep(2)
                #     horiz_slots[i].update()
                #     horiz_slots[i + 1].update()
                #     self.game.update()
                # horiz_slots[0].swap(horiz_slots[1])
                # horiz_slots[1].swap(horiz_slots[2])
                # for i in self.game.get_horizontal_slots():
                #     print("{} -> pile={}".format(i+1, i.pile))
                # self.slot.swap(slot)
                self.game.update()
                return
            for item in draggable_items:
                item.top = slot.top + draggable_items.index(item) * CARD_OFFSET
                item.left = slot.left
                if item.slot is not None:
                    item.slot.pile.remove(item)
                item.slot = slot
                slot.pile.append(item)
                # self.game.update()
                # slot.update()

        except Exception as e:
            pass
        # if slot.can_place(self):
        #     self.top = slot.top
        #     self.left = slot.left
        #     if self.slot is not None:
        #         self.slot.pile.remove(self)
        #     self.slot = slot
        #     slot.pile.append(self)
        # self.game.update()

    def start_drag(self, e: ft.DragStartEvent):
        # TODO : add the slot pile to the game instance to remove the card/pawn from it after drop is completed
        self.game.start_top = e.control.top
        self.game.start_left = e.control.left
        self.move_on_top()
        # self.update()
        self.game.update()

    def drag(self, e: ft.DragUpdateEvent):
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
                return
        self.bounce_back()
        # self.update()
        self.game.update()

    def get_draggable_items(self) -> list:
        """returns the card with the pawn on it"""
        return self.slot.pile[self.slot.pile.index(self):] if self.slot is not None else [self]
        if self.slot is not None:
            return self.slot.pile[-1]


class Pawn(Card):
    def __init__(self, game, card: Card, top, left, color, border_radius=50):
        super().__init__(game=game, color=color, border_radius=border_radius)
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
        # print("after_place_pawn", "dest_slot_pile={}, pawn_slot_pile={}".format(slot.pile, self.slot.pile))
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
    def __init__(self):
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
        self.create_cards()

    # method that returns the slots of the current horizontal line according to the start_top attribute
    def get_horizontal_slots(self) -> list:
        """Returns the slots of the current horizontal line according to the start_top attribute"""
        return [slt for slt in self.slots if slt.top == self.start_top]

    # method that returns the slots of the current vertical line according to the start_left attribute

    def get_vertical_slots(self) -> list:
        """Returns the slots of the current vertical line according to the start_left attribute"""
        return [slt for slt in self.slots if slt.left == self.start_left]

    def create_cards(self):
        # create 9 slots
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

        for i in range(9):
            if i == 4:
                continue
            self.game_cards[i].place(self.slots[i])
            # print("create_cards", "pile={}".format(self.slots[i].pile))

        for i in range(3):
            self.pawn1_cards[i].init(self.pawn_slot1[i])
            self.pawn2_cards[i].init(self.pawn_slot2[i])

        self.controls.extend(self.slots)
        self.controls.extend(self.game_cards)
        self.controls.extend(self.pawn_slot1)
        self.controls.extend(self.pawn_slot2)
        self.controls.extend(self.pawn1_cards)
        self.controls.extend(self.pawn2_cards)
        self.initiating = False


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
    force3 = Game()
    page.add(force3)
    page.update()


ft.app(name="Force3", target=main)

# from datetime import time
# import time as tm
# from force3 import Game
# import flet as ft
# from copy import deepcopy
# from model import Force3, minimax
#
# CARD_WIDTH = 70
# CARD_HEIGTH = 100
# CARD_OFFSET = 20
#
#
# class Card(ft.GestureDetector):
#
#     def __init__(self, game, slot=None, color=None, border_radius=0, height=CARD_HEIGTH, width=CARD_WIDTH):
#         super().__init__()
#         self.slot = slot
#         self.mouse_cursor = ft.MouseCursor.MOVE
#         self.drag_interval = 5
#         self.on_pan_start = self.start_drag
#         self.on_pan_update = self.drag
#         self.on_pan_end = self.drop
#         self.left = None
#         self.top = None
#         # self.pawn = None
#         self.game = game
#         self.color = color
#         self.content = ft.Container(bgcolor=self.color, width=width, height=height,
#                                     border_radius=border_radius)
#
#     def move_on_top(self):
#         """Moves draggable card to the top of the stack"""
#         for item in self.get_draggable_items():
#             self.game.controls.remove(item)
#             self.game.controls.append(item)
#             self.game.update()
#         try:
#             self.game.update()
#         except:
#             pass
#
#     def bounce_back(self):
#         """Returns card to its original position"""
#         try:
#             draggable_items = self.get_draggable_items()
#             for item in draggable_items:
#                 item.top = self.game.start_top + draggable_items.index(item) * CARD_OFFSET
#                 item.left = self.game.start_left
#                 board = [[-1, 2, 2], [-1, 0, -1], [-1, 1, 1]]
#
#         except:
#             self.top = self.top
#             self.left = self.left
#         # try:
#         self.game.update()
#         # self.update()
#
#     def place(self, slot):
#         """Place card to the slot"""
#         draggable_items = self.get_draggable_items()
#         # TODO : check if it is a two move action. If it is then move the pawns on the line
#         try:
#
#             # check if we can move two slots contents from left to right
#             if not self.game.initiating and slot.left == 0 and self.game.start_left == 200 and slot.top == self.slot.top:
#                 # swap the slots
#                 print("===> right to left")
#                 print(self.game.nb_moves_after_two_moves)
#                 if not self.game.can_make_hor_two_moves:
#                     self.bounce_back()
#                     return
#
#                 draggables = self.get_draggable_items()
#                 for el in draggables:
#                     el.left = self.game.start_left - 100
#                     el.top = slot.top + draggables.index(el) * CARD_OFFSET
#                     self.game.update()
#                 self.slot.left = self.game.start_left - 100  # mettre a jour le 100 en même temps ???
#                 self.game.update()
#                 slot.left = self.game.start_left
#                 slot.update()
#                 "The following commented code's purpose was to reset the middle slot's pile elements to their correct " \
#                 "top position"
#                 slot_els = slot.pile
#                 for el in slot_els:
#                     el.left = self.game.start_left
#                     el.top = slot.top + slot_els.index(el) * CARD_OFFSET
#                 # el.update()
#                 self.game.update()
#                 self.game.start_top = slot.top
#                 horiz_slots = self.game.get_horizontal_slots()
#                 # sort by left
#                 horiz_slots.sort(key=lambda x: x.left, reverse=True)
#                 horiz_slots = horiz_slots[1]
#                 horiz_slots.left = 0
#                 horiz_slots.update()
#                 middle_items = horiz_slots.pile
#                 for el in middle_items:
#                     el.left = 0
#
#                 reset_slots = self.game.get_horizontal_slots()
#                 reset_slots[0] = horiz_slots
#                 index = 3 * (-1 + self.game.start_top // 110)
#                 self.game.slots[index] = horiz_slots
#                 reset_slots[1] = self.slot
#                 self.game.slots[index + 1] = self.slot
#                 reset_slots[2] = slot
#                 self.game.slots[index + 2] = slot
#
#                 self.game.update()
#                 # update the two moves counter
#                 self.game.nb_moves_after_two_moves = 1
#                 self.game.can_make_hor_two_moves = False
#                 self.game.can_make_vert_two_moves = True
#
#                 return
#
#             # check if we can move two slots contents from right to left
#             if not self.game.initiating and slot.left == 200 and self.game.start_left == 0 and slot.top == self.slot.top:
#                 print("===> left to right")
#                 print(self.game.nb_moves_after_two_moves)
#                 if not self.game.can_make_hor_two_moves:
#                     self.bounce_back()
#                     return
#
#                 draggables = self.get_draggable_items()
#                 for el in draggables:
#                     el.left = self.game.start_left + 100
#                     # TODO : place thee elements at the right top position
#                     el.top = slot.top
#                     self.game.update()
#                 self.slot.left = self.game.start_left + 100  # mettre a jour le 100 en même temps ???
#                 self.game.update()
#                 slot.left = self.game.start_left
#                 # slot.update()
#                 slot_els = slot.pile
#                 for el in slot_els:
#                     el.left = self.game.start_left
#                     # el.update()
#                 self.game.update()
#                 # self.game.update()
#                 # get the horizontal slots
#                 horiz_slots = self.game.get_horizontal_slots()
#                 # sort by left
#                 horiz_slots.sort(key=lambda x: x.left, reverse=True)
#                 horiz_slots = horiz_slots[1]
#                 horiz_slots.left = 200
#                 horiz_slots.update()
#                 middle_items = horiz_slots.pile
#                 for el in middle_items:
#                     el.left = 200
#
#                 reset_slots = self.game.get_horizontal_slots()
#                 reset_slots[0] = horiz_slots
#                 index = 3 * (-1 + self.game.start_top // 110)
#                 self.game.slots[index] = slot
#                 reset_slots[1] = self.slot
#                 self.game.slots[index + 1] = self.slot
#                 reset_slots[2] = slot
#                 self.game.slots[index + 2] = horiz_slots
#
#                 self.game.update()
#                 # update the two moves counter
#                 self.game.nb_moves_after_two_moves = 1
#                 self.game.can_make_hor_two_moves = False
#                 self.game.can_make_vert_two_moves = True
#                 return
#
#             # check if we can move two slots contents from up to down
#             if not self.game.initiating and slot.top == 330 and self.game.start_top == 110 and slot.left == self.slot.left:
#                 print("===> up to down")
#                 print(self.game.nb_moves_after_two_moves)
#                 if not self.game.can_make_vert_two_moves:
#                     self.bounce_back()
#                     return
#
#                 draggables = self.get_draggable_items()
#                 for el in draggables:
#                     el.top = self.game.start_top + 110
#                     # TODO : place thee elements at the right top position
#                     el.left = slot.left
#                     self.game.update()
#                 self.slot.top = self.game.start_top + 110
#                 self.game.update()
#                 slot.top = self.game.start_top
#                 # slot.update()
#                 slot_els = slot.pile
#                 for el in slot_els:
#                     el.top = self.game.start_top
#                     # el.update()
#                 self.game.update()
#                 # self.game.update()
#                 # get the horizontal slots
#                 vert_slots = self.game.get_vertical_slots()
#                 # sort by left
#                 vert_slots.sort(key=lambda x: x.top, reverse=True)
#                 vert_slots = vert_slots[1]
#                 vert_slots.top = 330
#                 vert_slots.update()
#                 middle_items = vert_slots.pile
#                 for el in middle_items:
#                     el.top = 330
#                 reset_slots = self.game.get_vertical_slots()
#                 reset_slots[0] = vert_slots
#                 index = self.game.start_left // 100
#                 self.game.slots[index] = slot
#                 reset_slots[1] = self.slot
#                 self.game.slots[index + 3] = self.slot
#                 reset_slots[2] = slot
#                 self.game.slots[index + 6] = vert_slots
#
#                 self.game.update()
#                 # update the two moves counter
#                 self.game.nb_moves_after_two_moves = 1
#                 self.game.can_make_vert_two_moves = False
#                 self.game.can_make_hor_two_moves = True
#                 return
#
#             # check if we can move two slots contents from down to up
#             if not self.game.initiating  and slot.top == 110 and self.game.start_top == 330 and slot.left == self.slot.left:
#                 print("===> down to up")
#                 print(self.game.nb_moves_after_two_moves)
#                 if not self.game.can_make_vert_two_moves:
#                     self.bounce_back()
#                     return
#                 draggables = self.get_draggable_items()
#                 for el in draggables:
#                     el.top = self.game.start_top - 110
#                     # TODO : place thee elements at the right top position
#                     el.left = slot.left
#                     self.game.update()
#                 self.slot.top = self.game.start_top - 110
#                 self.game.update()
#                 slot.top = self.game.start_top
#                 # slot.update()
#                 slot_els = slot.pile
#                 for el in slot_els:
#                     el.top = self.game.start_top
#                     # el.update()
#                 self.game.update()
#                 # self.game.update()
#                 # get the horizontal slots
#                 vert_slots = self.game.get_vertical_slots()
#                 # sort by left
#                 vert_slots.sort(key=lambda x: x.top, reverse=True)
#                 vert_slots = vert_slots[1]
#                 vert_slots.top = 110
#                 vert_slots.update()
#                 middle_items = vert_slots.pile
#                 for el in middle_items:
#                     el.top = 110
#                 reset_slots = self.game.get_vertical_slots()
#                 reset_slots[0] = vert_slots
#                 index = self.game.start_left // 100
#                 self.game.slots[index] = vert_slots
#                 reset_slots[1] = self.slot
#                 self.game.slots[index + 3] = self.slot
#                 reset_slots[2] = slot
#                 self.game.slots[index + 6] = slot
#
#                 self.game.update()
#                 # update the two moves counter
#                 self.game.nb_moves_after_two_moves = 1
#                 self.game.can_make_vert_two_moves = False
#                 self.game.can_make_hor_two_moves = True
#                 return
#
#             # One move handler
#             for item in draggable_items:
#                 item.top = slot.top + draggable_items.index(item) * CARD_OFFSET
#                 item.left = slot.left
#                 if item.slot is not None:
#                     item.slot.pile.remove(item)
#                 item.slot = slot
#                 slot.pile.append(item)
#                 # update the two moves counter
#                 self.game.nb_moves_after_two_moves = 0
#                 self.game.can_make_hor_two_moves = True
#                 self.game.can_make_vert_two_moves = True
#
#         except Exception as e:
#             pass
#
#     def start_drag(self, e: ft.DragStartEvent):
#         # TODO : add the slot pile to the game instance to remove the card/pawn from it after drop is completed
#         # disable the drag if it is not the current player's turn
#
#         self.game.start_top = e.control.top
#         self.game.start_left = e.control.left
#         self.move_on_top()
#         # self.update()
#         self.game.update()
#
#     def drag(self, e: ft.DragUpdateEvent):
#         if not self.game.is_current_player_pawn(self):
#             self.bounce_back()
#             return
#         draggable_items = self.get_draggable_items()
#         for item in draggable_items:
#             # print("offset = {}".format(draggable_items.index(item) * CARD_OFFSET))
#             item.top = max(0, item.top + e.delta_y)  # + draggable_items.index(item) * CARD_OFFSET
#             item.left = max(0, item.left + e.delta_x)
#             self.game.update()
#
#         self.game.update()
#
#     def drop(self, e: ft.DragEndEvent):
#         for slot in self.game.slots:
#             if (
#                     abs(self.top - slot.top) < 20
#                     and abs(e.control.left - slot.left) < 20
#             ):
#                 if slot.can_place(self):
#                     self.place(slot)
#                 else:
#                     self.bounce_back()
#                 # self.update()
#                 self.game.update()
#                 print("board = {}".format(self.game.convert_game_to_force3_board()))
#                 board = [[-1, 2, 2], [-1, 0, -1], [-1, 1, 1]]
#                 # self.game.draw_board(board)
#                 # print("board = {}".format(self.game.convert_game_to_force3_board()))
#                 # print("is_game_over = {}".format(self.game.is_game_over()))
#                 if self.game.is_game_over():
#                     # TODO : show dialog with winner
#                     # print("The winner is : {}".format(self.game.ai_model.get_winner(self.game.convert_game_to_force3_board())))
#                     self.game.show_game_over_dialog()
#
#                 self.game.current_player = 3 - self.game.current_player
#                 print("next_player = {}".format(self.game.current_player))
#                 # if it is the AI's turn, then play
#                 if self.game.current_player == 2:
#                     # TODO : call the AI method to play
#                     # call model to play
#                     # delete the controls
#                     # make a deepcopy of the game
#                     state = self.game.convert_game_to_force3_board()
#                     board = minimax(self.game.ai_model, state, True, depth=4)[1]
#                     new_game = Game(plateau=board,page=self.game.page, vert_moves=self.game.can_make_vert_two_moves, hor_moves=self.game.can_make_hor_two_moves, current_player=self.game.current_player)
#                     self.game.page.controls.remove(self.game)
#                     self.game.page.update()
#                     # deep_copy = deepcopy(self.game)
#                     new_game.page.add(new_game)
#                     # self.game.page.update()
#                     new_game.page.update()
#                     #check if the game is over
#                     if new_game.is_game_over():
#                         # TODO : show dialog with winner
#                         # print("The winner is : {}".format(self.game.ai_model.get_winner(self.game.convert_game_to_force3_board())))
#                         new_game.show_game_over_dialog()
#
#
#                     self.game.delete_controls()
#                     del self.game
#                     # self.game.ai_play()
#                     # self.game.page.add(self.game)
#                 return
#         self.bounce_back()
#         # print board
#         # self.update()
#         self.game.update()
#
#     def get_draggable_items(self) -> list:
#         """returns the card with the pawn on it"""
#         try:
#             return self.slot.pile[self.slot.pile.index(self):] if self.slot is not None else [self]
#         except:
#             return [self]
#         if self.slot is not None:
#             return self.slot.pile[-1]
#

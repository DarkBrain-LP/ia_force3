# import flet as ft

# # Use of GestureDetector for with on_pan_update event for dragging card
# # Absolute positioning of controls within stack
# class Card(ft.GestureDetector):
#     def __init__(self, solitaire, color):
#         super().__init__()
#         self.slot = None
#         self.mouse_cursor=ft.MouseCursor.MOVE
#         self.drag_interval=5
#         self.on_pan_start=self.start_drag
#         self.on_pan_update=self.drag
#         self.on_pan_end=self.drop
#         self.left=None
#         self.top=None
#         self.solitaire = solitaire
#         self.color = color
#         self.content=ft.Container(bgcolor=self.color, width=CARD_WIDTH, height=CARD_HEIGTH)

#     def move_on_top(self):
#         """Moves draggable card to the top of the stack"""
#         self.solitaire.controls.remove(self)
#         self.solitaire.controls.append(self)
#         self.solitaire.update()

#     def bounce_back(self):
#         """Returns card to its original position"""
#         self.top = self.slot.top
#         self.left = self.slot.left
#         self.update()
    
#     def place(self, slot):
#         """Place card to the slot"""
#         self.top = slot.top
#         self.left = slot.left
#         self.slot = slot
        
#     def place(self, slot):
#     # remove card from it's original slot, if exists
#         if self.slot is not None:
#             self.slot.pile.remove(self)
        
#         # change card's slot to a new slot
#         self.slot = slot

#         # add card to the new slot's pile
#         slot.pile.append(self)

#     def start_drag(self, e: ft.DragStartEvent):
#         self.move_on_top()
#         self.update()

    
#     def drag(self, e: ft.DragUpdateEvent):
#         self.top = max(0, self.top + e.delta_y)
#         self.left = max(0, self.left + e.delta_x)
#         self.update()

#     def drop(self, e: ft.DragEndEvent):
#         for slot in self.solitaire.slots:
#             if (
#                 abs(e.control.top - slot.top) < 20
#             and abs(e.control.left - slot.left) < 20
#             ):
#                 place(e.control, slot)
#                 e.control.update()
#                 return
            
#         bounce_back(solitaire, e.control)
#         e.control.update()
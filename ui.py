import flet as ft
 
# Use of GestureDetector for with on_pan_update event for dragging card
# Absolute positioning of controls within stack

class Solitaire:
   def __init__(self):
       self.start_top = 0
       self.start_left = 0

# solitaire = Solitaire()




def main(page: ft.Page):
 
    def bounce_back(game, card):
        """return card to its original position"""
        print("repousse : {} {}".format(game.start_top, game.start_left))
        card.top = game.start_top
        card.left = game.start_left
        page.update()
    
    def move_on_top(card, controls):
        """Moves draggable card to the top of the stack"""
        controls.remove(card)
        controls.append(card)
        page.update()

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, controls)
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left
        e.control.update()
    
    def drag(e: ft.DragUpdateEvent):
    #    print(e.delta_x, e.delta_y)
       e.control.top = max(0, e.control.top + e.delta_y)
       e.control.left = max(0, e.control.left + e.delta_x)
       e.control.update()
       
    def drop(e: ft.DragEndEvent):
        for slot in slots:
            if (
                abs(e.control.top - slot.top) < 20
            and abs(e.control.left - slot.left) < 20
            ):
                print(e.control.content)
                # print the background color of the slot
                
                if e.control.content.content is None:
                    print("None")
                    place(e.control, slot)
                    e.control.update()
                return
            
        bounce_back(solitaire, e.control)
        e.control.update()

    def place(card, slot):
        """place card to the slot"""
        card.top = slot.top
        card.left = slot.left
        
        page.update()

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        # left=0,
        # top=0,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=70, height=100),
    )

        
    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        # left=100,
        # top=0,
        content=ft.Container(bgcolor=ft.colors.YELLOW, width=70, height=100),
    )

    slot0 = ft.Container(
    width=70, height=100, left=0, top=0, border=ft.border.all(1)
    )

    slot1 = ft.Container(
        width=70, height=100, left=200, top=0, border=ft.border.all(1)
    )

    slot2 = ft.Container(
        width=70, height=100, left=300, top=0, border=ft.border.all(1)
    )

    slots = [slot0, slot1, slot2]
    # create 9 cards
    cards = []
    for i in range(9):
        cards.append(ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=50,
            on_pan_start=start_drag,
            on_pan_update=drag,
            on_pan_end=drop,
            # left=100,
            # top=0,
            content=ft.Container(bgcolor=ft.colors.BROWN, width=70, height=100),
        ))


    # create 9 slots
    slots = []
    delta_x = 100
    for i in range(3):
        for j in range(3):
            slots.append(ft.Container(
                width=70, height=100, left=100*j, top=delta_x, border=ft.border.all(1)
            ))
        delta_x += 110

    pawns1 = []
    pawns2 = []
    for i in range(3):
        pawns1.append(ft.Container(
            width=70, height=100, left=100*i, top=0, border=ft.border.all(1)
        ))
    
    for i in range(3):
        pawns2.append(ft.Container(
            width=70, height=100, left=100*i, top=500, border=ft.border.all(1)
        ))

    pawn1_cards = []
    pawn2_cards = []
    for i in range(3):
        pawn1_cards.append(ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=10,
            on_pan_start=start_drag,
            on_pan_update=drag,
            on_pan_end=drop,
            # left=100,
            # top=0,
            content=ft.Container(bgcolor=ft.colors.RED, width=50, height=50, border_radius=50),
        ))
        # append(ft.Container(
        #     width=30, height=30, left=100*i, top=0, bgcolor=ft.colors.RED, border=ft.border.all(1)
        # ))

    for i in range(3):
        pawn2_cards.append(ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=10,
            on_pan_start=start_drag,
            on_pan_update=drag,
            on_pan_end=drop,
            # left=100,
            # top=0,
            content=ft.Container(bgcolor=ft.colors.BLUE, width=50, height=50, border_radius=50),
        ))
        
    # slots.append(ft.Container(width=70, height=100, left=0, top=100, bgcolor=ft.colors.BLUE_GREY_200))
    # place cards in slots
    for i in range(9):
        place(cards[i], slots[i])

    for i in range(3):
        place(pawn1_cards[i], pawns1[i])
        place(pawn2_cards[i], pawns2[i])
    
    controls = []
    controls.append(pawns1)
    controls.append(pawns2)
    controls.extend(pawn1_cards)
    controls.extend(pawn2_cards)
    # add slots to page
    controls.append(slots)
    # add pawns to page
    # add cards to page
    controls.extend(cards)
    # deal cards
    # place(card1, slot0)
    # place(card2, slot0)

    solitaire = Solitaire()
    stack = ft.Stack(width=700, height=700)
    stack.controls.extend(slots)
    stack.controls.extend(pawns1)
    stack.controls.extend(pawns2)
    stack.controls.extend(pawn1_cards)
    stack.controls.extend(pawn2_cards)
    stack.controls.extend(cards)
    # page.add(ft.Stack(controls = [slot, card], width=1000, height=500))
    page.add(stack)

    # get the middle card and move it to the top of the stack
    card = stack.controls[4]
    print(card.border.top.color)
    #set its border to none
    # card.border = ft.border.all(0, ft.colors.WHITE)
    card.border.top.width = 0
    card.border.left.width = 0
    print(card.border)
    stack.controls.remove(cards[4])
    stack.update()
    
    
    
ft.app(target=main)
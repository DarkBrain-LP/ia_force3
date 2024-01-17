import time as tm
import flet as ft
from model import Force3, minimax

#from ui.card import Card
# from ui.pawn import Pawn
# from ui.slot import Slot

CARD_WIDTH = 70
CARD_HEIGTH = 100
CARD_OFFSET = 20
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
        self.ai_model = Force3()  # [[1, -1, -1],
        #         [-1, -1, -1],
        #         [0, -1, 2]]
        self.create_cards(plateau)  # self.ai_model.plateau
        self.page = page
        # self.ai_game()

    def ai_play(self):
        self.ai_model.current_player = 2
        self.ai_model.plateau = self.convert_game_to_force3_board()
        board = minimax(self.ai_model, self.ai_model.plateau, True, depth=3)[1]
        self.ai_model.plateau = board
        self.create_cards(board, self.can_make_vert_two_moves, self.can_make_hor_two_moves, 1)
        self.update()

    def ai_game(self):
        """AI vs AI game"""
        new_game = None
        while not self.is_game_over():
            state = self.convert_game_to_force3_board()
            board = minimax(self.ai_model, state, self.ai_model.current_player % 2 == 0, depth=4)[1]
            new_game = Game(plateau=board, page=self.page, vert_moves=self.can_make_vert_two_moves,
                            hor_moves=self.can_make_hor_two_moves, current_player=self.current_player)
            self.page.controls.remove(self.game)
            self.page.update()
            # deep_copy = deepcopy(self.game)
            new_game.page.add(new_game)
            # self.game.page.update()
            new_game.page.update()
            tm.sleep(3)
            # check if the game is over
            self.ai_model.current_player += 1
        new_game.show_game_over_dialog()

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

    def create_cards(self, board: list[list[int]] = None, vert_moves=False, hor_moves=False, current_player=1):
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
                    pos = 3 * i + j
                    if board[i][j] == 0:  # si l'élément est vide, on ne pose pas de carré
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
            non_played_red_pawns = 3 - len(played_red_pawns)
            non_played_blue_pawns = 3 - len(played_blue_pawns)
            pawn1_index = 2
            pawn2_index = 2
            for i in range(non_played_red_pawns):
                self.pawn1_cards[pawn1_index].init(self.pawn_slot1[pawn1_index])
                pawn1_index -= 1
                played_red_pawns.append(2)
            for i in range(non_played_blue_pawns):  # here, non_played_blue_pawns-1 items will be initialized
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
                pos = 3 * i + j
                if board[i][j] == 0:  # si l'élément est vide, on ne pose pas de carré
                    continue
                self.game_cards[pos].place(self.slots[pos])
            # print("create_cards", "pile={}".format(self.slots[i].pile))

        # now we will place the items according to the board
        # place the pawns that are not on the board to their initial position
        played_red_pawns = [item for sublist in board for item in sublist if item == 2]
        played_blue_pawns = [item for sublist in board for item in sublist if item == 1]
        non_played_red_pawns = 3 - len(played_red_pawns)
        non_played_blue_pawns = 3 - len(played_blue_pawns)
        for i in range(non_played_red_pawns):
            self.pawn1_cards[i].init(self.pawn_slot1[i])
            played_red_pawns.append(2)
        for i in range(non_played_blue_pawns):  # here, non_played_blue_pawns-1 items will be initialized
            self.pawn2_cards[i].init(self.pawn_slot2[i])
            played_blue_pawns.append(1)
        # for i in range(3):
        #     self.pawn1_cards[i].init(self.pawn_slot1[i])
        #     self.pawn2_cards[i].init(self.pawn_slot2[i])

        for i in range(3):
            for j in range(3):
                value = board[i][j]
                if value == 1:
                    self.pawn2_cards[non_played_blue_pawns + 1].place(self.slots[i * 3 + j])
                    non_played_blue_pawns += 1
                elif value == 2:
                    self.pawn1_cards[non_played_red_pawns + 1].place(self.slots[i * 3 + j])
                    non_played_red_pawns += 1

        self.controls.extend(self.slots)
        self.controls.extend(self.game_cards)
        self.controls.extend(self.pawn_slot1)
        self.controls.extend(self.pawn_slot2)
        self.controls.extend(self.pawn1_cards)
        self.controls.extend(self.pawn2_cards)
        self.initiating = False

    def convert_game_to_force3_board(self) -> list[list[int]]:
        board = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

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
                        else:
                            board[i][j] = 1  # Represent a pawn

        return board

    def is_game_over(self) -> bool:
        """Returns True if the game is over"""
        board = self.convert_game_to_force3_board()
        print("is_game_over", "board={}".format(board))
        return self.ai_model.isFinal(board)

    def show_game_over_dialog(self):
        """Shows a dialog when the game is over"""
        tm.sleep(2)
        global is_game_over
        is_game_over = True
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()

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

    def close_dlg(self, e):
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


# flet main
def main(page: ft.Page):
    force3 = Game(page=page)
    global is_game_over

    def ai_play(e):
        close_dlg(None)
        force3 = Game(page=page)
        page.add(force3)
        page.update()
        new_game = None
        turn = 0

        # global force3
        while not force3.is_game_over():
            state = force3.convert_game_to_force3_board()
            board = minimax(force3.ai_model, state, turn % 2 == 0, depth=5)[1]
            new_game = Game(plateau=board, page=force3.page, vert_moves=force3.can_make_vert_two_moves,
                            hor_moves=force3.can_make_hor_two_moves, current_player=turn % 2 + 1)
            page.controls.remove(force3)
            page.update()
            # deep_copy = deepcopy(force3.game)
            force3 = new_game
            page.add(force3)
            # force3.game.page.update()
            page.update()
            tm.sleep(3)
            # check if the game is over
            # force3.ai_model.current_player += 1
            turn += 1
        new_game.show_game_over_dialog()

    def user_play(e):
        close_dlg(None)
        force3 = Game(page=page)
        page.add(force3)
        page.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    end_of_game_txt = "La partie est terminée ! "
    global dlg_modal
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Type de jeu {is_game_over}"),
        content=ft.Text(f"{end_of_game_txt if is_game_over else ''}Voulez-vous voir l'IA jouer contre elle-même ?"),
        actions=[
            ft.TextButton("Oui", on_click=ai_play),
            ft.TextButton("Non", on_click=user_play),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def open_dlg_modal(e=None):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def show_game_over_dialog(e):
        is_game_over = True
        open_dlg_modal()

    open_dlg_modal()
    # page.add(
    #     ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
    # )

    # page.add(force3)

    # page.update()


dlg_modal = None
is_game_over = False

ft.app(name="Force3", target=main)

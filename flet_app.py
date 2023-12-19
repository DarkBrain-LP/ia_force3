import time
import flet as ft

def main(page: ft.Page):
    page.title = "Force 3"
    
    # page.body = ft.Div(
    #     ft.H1("Flet"),
    #     ft.P("Flet is a web framework for Python."),
    #     ft.P("This is a sample page."))
    # t = ft.Text(value="Hello, world!", color="red")
    # page.controls.append(t)
    # page.update()

    # t = ft.Text()
    # page.add(t) # it's a shortcut for page.controls.append(t) and then page.update()

    # for i in range(10):
    #     t.value = f"Step {i}"
    #     page.update()
    #     time.sleep(0.2)

    # # for i in range(10):
    # #     page.controls.append(ft.Text(f"Line {i}"))
    # #     if i > 4:
    # #         page.controls.pop(0)
    # #     page.update()
    # #     time.sleep(0.3)

    # page.add(
    #     ft.Row(controls=[
    #         ft.Text("A"),
    #         ft.Text("B"),
    #         ft.Text("C")
    #     ])
    # )

    # page.add(
    #     ft.Row(controls=[
    #         ft.TextField(label="Your name"),
    #         ft.ElevatedButton(text="Say my name!")
    #     ])
    # )

    # def add_clicked(e):
    #     page.add(ft.Checkbox(label=new_task.value))
    #     new_task.value = ""
    #     new_task.focus()
    #     new_task.update()

    # new_task = ft.TextField(hint_text="Whats needs to be done?", width=300)
    # page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))

    # grid = ft.GridView(width=3, height=3)
    # page.add(grid)
    # for i in range(3):
    #     row = ft.Row()
    #     for j in range(3):
    #         row.controls.append(ft.Draggable(content=ft.Text(f"({i}, {j})")))
    #     grid.controls.append(row)
    #     grid.update()
    #     page.update()
    # page.add(grid)

    def drag_accept(e):
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
        # update text inside draggable control
        src.content.content.value = "0"
        # update text inside drag target control
        e.control.content.content.value = "1"
        page.update()

    page.add(
        ft.Row(
            [
                ft.Draggable(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.CYAN_200,
                        border_radius=5,
                        content=ft.Text("1", size=20),
                        alignment=ft.alignment.center,
                    ),
                    content_when_dragging=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.BLUE_GREY_200,
                        border_radius=5,
                    ),
                    content_feedback=ft.Text("1"),
                ),
                ft.Container(width=100),
                ft.DragTarget(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.PINK_200,
                        border_radius=5,
                        content=ft.Text("0", size=20),
                        alignment=ft.alignment.center,
                    ),
                    on_accept=drag_accept,
                ),
            ]
        )
    )
ft.app(target=main)
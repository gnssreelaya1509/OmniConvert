# app.py
import flet as ft
from core.engine import CalculatorEngine


def main(page: ft.Page):
    page.title = "OmniConvert"
    page.window.width = 360
    page.window.height = 560
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.END

    engine = CalculatorEngine()

    # FIX 1: Swapped to an ft.Text component to allow infinite leftward scrolling text flow
    display_text = ft.Text(
        value="",
        size=34,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.W_400,
        max_lines=1,
    )

    display_container = ft.Container(
        content=display_text,
        alignment=ft.Alignment.CENTER_RIGHT,
        padding=10,
        bgcolor=ft.Colors.BLACK_12,
        height=70,
        border_radius=8
    )

    def process_input(data):
        if data == "C":
            display_text.value = ""
        elif data == "=":
            try:
                res = engine.calculate_expression(display_text.value)
                display_text.value = str(int(res)) if res.is_integer() else str(res)
            except Exception:
                display_text.value = "Error"
        elif data == "BACKSPACE":
            if display_text.value not in ["", "Error"]:
                display_text.value = display_text.value[:-1]
        else:
            if display_text.value == "Error":
                display_text.value = ""
            display_text.value += str(data)

        page.update()

    def button_click(e):
        process_input(e.control.data)

    def on_keyboard(e: ft.KeyboardEvent):
        # FIX 2: Intercept Shift modifiers early to capture symbols instead of raw numbers
        if e.shift:
            if e.key == "9":
                process_input("(")
                return
            elif e.key == "0":
                process_input(")")
                return
            elif e.key == "8":
                process_input("*")
                return
            elif e.key == "=":
                process_input("+")
                return

        valid_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", ".", "(", ")"]

        numpad_map = {
            "Numpad 0": "0", "Numpad 1": "1", "Numpad 2": "2", "Numpad 3": "3",
            "Numpad 4": "4", "Numpad 5": "5", "Numpad 6": "6", "Numpad 7": "7",
            "Numpad 8": "8", "Numpad 9": "9",
            "Numpad .": ".", "Numpad Decimal": ".",
            "Numpad +": "+", "Numpad Add": "+",
            "Numpad -": "-", "Numpad Subtract": "-",
            "Numpad *": "*", "Numpad Multiply": "*",
            "Numpad /": "/", "Numpad Divide": "/",
            "Numpad Enter": "="
        }

        if e.key in valid_chars:
            process_input(e.key)
        elif e.key in numpad_map:
            process_input(numpad_map[e.key])
        elif e.key == "Enter" or e.key == "=":
            process_input("=")
        elif e.key == "Escape":
            process_input("C")
        elif e.key == "Backspace":
            process_input("BACKSPACE")

    page.on_keyboard_event = on_keyboard

    def build_btn(text, color=ft.Colors.GREY_800, text_color=ft.Colors.WHITE):
        return ft.Container(
            content=ft.Text(value=text, size=24, color=text_color, weight=ft.FontWeight.W_600),
            alignment=ft.Alignment.CENTER,
            bgcolor=color,
            border_radius=50,
            on_click=button_click,
            data=text,
            expand=1,
            height=75,
        )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    display_container,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row(controls=[build_btn("C", ft.Colors.AMBER_900), build_btn("(", ft.Colors.GREY_700),
                                     build_btn(")", ft.Colors.GREY_700), build_btn("/", ft.Colors.ORANGE_800)]),
                    ft.Row(controls=[build_btn("7"), build_btn("8"), build_btn("9"),
                                     build_btn("*", ft.Colors.ORANGE_800)]),
                    ft.Row(controls=[build_btn("4"), build_btn("5"), build_btn("6"),
                                     build_btn("-", ft.Colors.ORANGE_800)]),
                    ft.Row(controls=[build_btn("1"), build_btn("2"), build_btn("3"),
                                     build_btn("+", ft.Colors.ORANGE_800)]),
                    ft.Row(controls=[build_btn("0", ft.Colors.GREY_800), build_btn("."),
                                     build_btn("=", ft.Colors.GREEN_700)]),
                ],
                spacing=10
            ),
            padding=15
        )
    )


if __name__ == "__main__":
    ft.run(main)
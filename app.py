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

    display = ft.TextField(
        value="",
        text_align=ft.TextAlign.RIGHT,
        text_size=34,
        read_only=True,
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor=ft.Colors.BLACK_12
    )

    def button_click(e):
        data = e.control.data
        if data == "C":
            display.value = ""
        elif data == "=":
            try:
                res = engine.calculate_expression(display.value)
                display.value = str(int(res)) if res.is_integer() else str(res)
            except Exception:
                display.value = "Error"
        else:
            if display.value == "Error":
                display.value = ""
            display.value += str(data)
        page.update()

    def build_btn(text, color=ft.Colors.GREY_800, text_color=ft.Colors.WHITE):
        return ft.Container(
            content=ft.Text(value=text, size=24, color=text_color, weight=ft.FontWeight.W_600),
            # FIX: Capitalized the 'A' in Alignment
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
                    display,
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
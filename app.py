# app.py
import flet as ft
import re
from core.engine import CalculatorEngine


def main(page: ft.Page):
    page.title = "OmniConvert Professional Portfolio"
    page.window.width = 400
    page.window.height = 680
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK

    engine = CalculatorEngine()

    # Calculator State Memory Registers
    state = {
        "memory": 0.0,
        "last_was_equal": False,
        "repeat_op": "",
        "repeat_val": ""
    }

    # ==========================================
    # RESOURCE COMPONENT: CALCULATOR VIEW BUILDER
    # ==========================================
    display_text = ft.Text(value="", size=34, color=ft.Colors.WHITE, weight=ft.FontWeight.W_400, max_lines=1)
    display_row = ft.Row(controls=[display_text], alignment=ft.MainAxisAlignment.END, scroll=ft.ScrollMode.HIDDEN,
                         auto_scroll=True)
    display_container = ft.Container(content=display_row, alignment=ft.Alignment.CENTER_RIGHT, padding=12,
                                     bgcolor=ft.Colors.BLACK_12, height=75, border_radius=8)

    def process_input(data):
        current = display_text.value
        operators = ["+", "-", "*", "/"]

        if data == "C":
            display_text.value = ""
            state["last_was_equal"] = False
            state["repeat_op"] = ""
            state["repeat_val"] = ""
        elif data == "CE":
            tokens = re.split(r'([\+\-\*\/ \(\)])', current)
            if tokens:
                if tokens[-1] == "": tokens.pop()
                if tokens: tokens.pop()
                display_text.value = "".join(tokens)
        elif data == "BACKSPACE":
            if current not in ["", "Error"]:
                display_text.value = current[:-1]
        elif data in ["MC", "MR", "M+", "M-"]:
            try:
                eval_current = engine.calculate_expression(current if current else "0")
                if data == "MC":
                    state["memory"] = 0.0
                elif data == "MR":
                    mem_str = str(int(state["memory"])) if state["memory"].is_integer() else str(state["memory"])
                    display_text.value = current + mem_str
                elif data == "M+":
                    state["memory"] += eval_current
                elif data == "M-":
                    state["memory"] -= eval_current
            except Exception:
                display_text.value = "Error"
        elif data == "=":
            try:
                if state["last_was_equal"] and state["repeat_op"]:
                    expr_to_run = f"{current}{state['repeat_op']}{state['repeat_val']}"
                else:
                    expr_to_run = current
                    match = re.search(r'([\+\-\*\/])\s*([0-9.]+)%$', current)
                    if not match: match = re.search(r'([\+\-\*\/])\s*([0-9.]+)$', current)
                    if match:
                        state["repeat_op"] = match.group(1)
                        state["repeat_val"] = match.group(2) if "%" not in match.group(0) else match.group(2) + "%"

                res = engine.calculate_expression(expr_to_run)
                display_text.value = str(int(res)) if res.is_integer() else str(res)
                state["last_was_equal"] = True
            except Exception:
                display_text.value = "Error"
        else:
            if current == "Error": current = ""
            state["last_was_equal"] = False
            if data in operators and current != "":
                if current[-1] in operators:
                    display_text.value = current[:-1] + data
                    page.update()
                    return
            if data == ".":
                tokens = re.split(r'[\+\-\*\/ \(\)]', current)
                if tokens and "." in tokens[-1]:
                    page.update()
                    return
                if current == "" or current[-1] in operators or current[-1] == "(":
                    display_text.value += "0."
                    page.update()
                    return
            if data.isdigit() and current == "0":
                display_text.value = data
                page.update()
                return
            display_text.value += str(data)
        page.update()

    def build_calc_btn(text, color=ft.Colors.GREY_800, text_color=ft.Colors.WHITE):
        return ft.Container(
            content=ft.Text(value=text, size=20, color=text_color, weight=ft.FontWeight.W_600),
            alignment=ft.Alignment.CENTER,
            bgcolor=color,
            border_radius=50,
            on_click=lambda e: process_input(text),
            expand=1,
            height=60,
        )

    def on_keyboard(e: ft.KeyboardEvent):
        if page.route != "/calculator": return
        if e.shift:
            if e.key == "9":
                process_input("("); return
            elif e.key == "0":
                process_input(")"); return
            elif e.key == "8":
                process_input("*"); return
            elif e.key == "=":
                process_input("+"); return
            elif e.key == "5":
                process_input("%"); return
        valid_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", ".", "(", ")", "%"]
        numpad_map = {
            "Numpad 0": "0", "Numpad 1": "1", "Numpad 2": "2", "Numpad 3": "3", "Numpad 4": "4",
            "Numpad 5": "5", "Numpad 6": "6", "Numpad 7": "7", "Numpad 8": "8", "Numpad 9": "9",
            "Numpad .": ".", "Numpad Decimal": ".", "Numpad +": "+", "Numpad Add": "+",
            "Numpad -": "-", "Numpad Subtract": "-", "Numpad *": "*", "Numpad Multiply": "*",
            "Numpad /": "/", "Numpad Divide": "/", "Numpad Enter": "="
        }
        if e.key in valid_chars:
            process_input(e.key)
        elif e.key in numpad_map:
            process_input(numpad_map[e.key])
        elif e.key in ["Enter", "="]:
            process_input("=")
        elif e.key == "Escape":
            process_input("C")
        elif e.key == "Backspace":
            process_input("BACKSPACE")

    page.on_keyboard_event = on_keyboard

    # ==========================================
    # CORE SYSTEM ROUTING ENGINE
    # ==========================================
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()

        # VIEW A: THE PORTFOLIO HUB (Default Home)
        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.AppBar(title=ft.Text("My Engineering Hub"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                  center_title=True),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Select a tool to execute native operations:", size=16,
                                            color=ft.Colors.GREY_400),
                                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),

                                    # CARD 1: OMNICONVERT CALCULATOR
                                    ft.Card(
                                        content=ft.Container(
                                            content=ft.ListTile(
                                                leading=ft.Icon(ft.Icons.CALCULATOR, color=ft.Colors.GREEN_400,
                                                                size=32),
                                                title=ft.Text("OmniConvert Engine", weight=ft.FontWeight.BOLD),
                                                subtitle=ft.Text(
                                                    "Advanced arithmetic calculator with persistent operations and memory cache systems."),
                                            ),
                                            padding=10,
                                            # FIX 1: Swapped to page.navigate()
                                            on_click=lambda _: page.navigate("/calculator")
                                        )
                                    ),

                                    # CARD 2: PLACEHOLDER FOR NEXT SUB-SYSTEM DATA CONVERTER
                                    ft.Card(
                                        content=ft.Container(
                                            content=ft.ListTile(
                                                leading=ft.Icon(ft.Icons.DATA_OBJECT, color=ft.Colors.BLUE_400,
                                                                size=32),
                                                title=ft.Text("Developer Utilities (Locked)", color=ft.Colors.GREY_500),
                                                subtitle=ft.Text(
                                                    "Upcoming utility module to parse Base64, Hexadecimal formats, and serialize custom configurations."),
                                            ),
                                            padding=10,
                                        ),
                                        opacity=0.6
                                    )
                                ]
                            ),
                            padding=15
                        )
                    ]
                )
            )

        # VIEW B: THE INSTANTIATED CALCULATOR VIEW
        elif page.route == "/calculator":
            page.views.append(
                ft.View(
                    route="/calculator",
                    controls=[
                        ft.AppBar(title=ft.Text("OmniConvert Calculator"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    display_container,
                                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                                    ft.Row(controls=[build_calc_btn("MC", ft.Colors.BLUE_GREY_900),
                                                     build_calc_btn("MR", ft.Colors.BLUE_GREY_900),
                                                     build_calc_btn("M+", ft.Colors.BLUE_GREY_900),
                                                     build_calc_btn("M-", ft.Colors.BLUE_GREY_900)]),
                                    ft.Row(controls=[build_calc_btn("C", ft.Colors.AMBER_900),
                                                     build_calc_btn("CE", ft.Colors.BLUE_GREY_700),
                                                     build_calc_btn("%", ft.Colors.BLUE_GREY_700),
                                                     build_calc_btn("/", ft.Colors.ORANGE_800)]),
                                    ft.Row(controls=[build_calc_btn("7"), build_calc_btn("8"), build_calc_btn("9"),
                                                     build_calc_btn("*", ft.Colors.ORANGE_800)]),
                                    ft.Row(controls=[build_calc_btn("4"), build_calc_btn("5"), build_calc_btn("6"),
                                                     build_calc_btn("-", ft.Colors.ORANGE_800)]),
                                    ft.Row(controls=[build_calc_btn("1"), build_calc_btn("2"), build_calc_btn("3"),
                                                     build_calc_btn("+", ft.Colors.ORANGE_800)]),
                                    ft.Row(controls=[build_calc_btn("0"), build_calc_btn("."),
                                                     build_calc_btn("=", ft.Colors.GREEN_700)]),
                                ],
                                spacing=8
                            ),
                            padding=12
                        )
                    ]
                )
            )
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        # FIX 2: Swapped to page.navigate()
        page.navigate(top_view.route)

    # Bind Routing handlers to page actions
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # FIX 3: Swapped to page.navigate()
    page.navigate(page.route)


if __name__ == "__main__":
    ft.run(main)
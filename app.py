# app.py
import flet as ft
import re
from core.engine import CalculatorEngine


def main(page: ft.Page):
    page.title = "OmniConvert"
    page.window.width = 380
    page.window.height = 640
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.END

    engine = CalculatorEngine()

    # Commercial App State Management
    state = {
        "memory": 0.0,
        "last_was_equal": False,
        "repeat_op": "",
        "repeat_val": ""
    }

    display_text = ft.Text(value="", size=34, color=ft.Colors.WHITE, weight=ft.FontWeight.W_400, max_lines=1)

    display_row = ft.Row(controls=[display_text], alignment=ft.MainAxisAlignment.END, scroll=ft.ScrollMode.HIDDEN,
                         auto_scroll=True)

    display_container = ft.Container(content=display_row, alignment=ft.Alignment.CENTER_RIGHT, padding=12,
                                     bgcolor=ft.Colors.BLACK_12, height=75, border_radius=8)

    def process_input(data):
        current = display_text.value
        operators = ["+", "-", "*", "/"]

        # Handle Clear Instructions
        if data == "C":
            display_text.value = ""
            state["last_was_equal"] = False
            state["repeat_op"] = ""
            state["repeat_val"] = ""
        elif data == "CE":
            # FEATURE: Clear Entry - erases only the current trailing number block
            tokens = re.split(r'([\+\-\*\/ \(\)])', current)
            if tokens:
                if tokens[-1] == "": tokens.pop()  # Drop empty trails
                if tokens: tokens.pop()  # Clear last valid entry block
                display_text.value = "".join(tokens)
        elif data == "BACKSPACE":
            if current not in ["", "Error"]:
                display_text.value = current[:-1]

        # FEATURE: Memory Cache System
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

        # Handle Equals/Evaluation execution
        elif data == "=":
            try:
                # FEATURE: Persistent Constant Operation (Repeated Equals execution)
                if state["last_was_equal"] and state["repeat_op"]:
                    expr_to_run = f"{current}{state['repeat_op']}{state['repeat_val']}"
                else:
                    # Capture repeating parameters during first explicit compute
                    expr_to_run = current
                    match = re.search(r'([\+\-\*\/])\s*([0-9.]+)%$', current)  # match trailing percentage operations
                    if not match:
                        match = re.search(r'([\+\-\*\/])\s*([0-9.]+)$', current)
                    if match:
                        state["repeat_op"] = match.group(1)
                        state["repeat_val"] = match.group(2) if "%" not in match.group(0) else match.group(2) + "%"

                res = engine.calculate_expression(expr_to_run)
                display_text.value = str(int(res)) if res.is_integer() else str(res)
                state["last_was_equal"] = True
            except Exception:
                display_text.value = "Error"

        # Handle Standard Inputs
        else:
            if current == "Error": current = ""
            state["last_was_equal"] = False

            # FEATURE: Operator Overwriting Protection
            if data in operators and current != "":
                if current[-1] in operators:
                    display_text.value = current[:-1] + data
                    page.update()
                    return

            # FEATURE: Dynamic Decimal Point Guardrail
            if data == ".":
                tokens = re.split(r'[\+\-\*\/ \(\)]', current)
                if tokens and "." in tokens[-1]:
                    page.update()
                    return  # Ignore duplicate injection
                if current == "" or current[-1] in operators or current[-1] == "(":
                    display_text.value += "0."
                    page.update()
                    return

            # FEATURE: Smart Leading Zero Truncation
            if data.isdigit() and current == "0":
                display_text.value = data
                page.update()
                return

            display_text.value += str(data)

        page.update()

    def button_click(e):
        process_input(e.control.data)

    def on_keyboard(e: ft.KeyboardEvent):
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
            "Numpad 0": "0", "Numpad 1": "1", "Numpad 2": "2", "Numpad 3": "3",
            "Numpad 4": "4", "Numpad 5": "5", "Numpad 6": "6", "Numpad 7": "7",
            "Numpad 8": "8", "Numpad 9": "9", "Numpad .": ".", "Numpad Decimal": ".",
            "Numpad +": "+", "Numpad Add": "+", "Numpad -": "-", "Numpad Subtract": "-",
            "Numpad *": "*", "Numpad Multiply": "*", "Numpad /": "/", "Numpad Divide": "/",
            "Numpad Enter": "="
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

    def build_btn(text, color=ft.Colors.GREY_800, text_color=ft.Colors.WHITE):
        return ft.Container(
            content=ft.Text(value=text, size=20, color=text_color, weight=ft.FontWeight.W_600),
            alignment=ft.Alignment.CENTER,
            bgcolor=color,
            border_radius=50,
            on_click=button_click,
            data=text,
            expand=1,
            height=65,
        )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    display_container,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    # Row 1: Dedicated Memory Interface Engine
                    ft.Row(controls=[build_btn("MC", ft.Colors.BLUE_GREY_900), build_btn("MR", ft.Colors.BLUE_GREY_900),
                                     build_btn("M+", ft.Colors.BLUE_GREY_900),
                                     build_btn("M-", ft.Colors.BLUE_GREY_900)]),
                    # Row 2: Master Core System Utility Controls
                    ft.Row(controls=[build_btn("C", ft.Colors.AMBER_900), build_btn("CE", ft.Colors.BLUE_GREY_700),
                                     build_btn("%", ft.Colors.BLUE_GREY_700), build_btn("/", ft.Colors.ORANGE_800)]),
                    # Keypad standard array rows
                    ft.Row(controls=[build_btn("7"), build_btn("8"), build_btn("9"),
                                     build_btn("*", ft.Colors.ORANGE_800)]),
                    ft.Row(controls=[build_btn("4"), build_btn("5"), build_btn("6"),
                                     build_btn("-", ft.Colors.ORANGE_800)]),
                    ft.Row(controls=[build_btn("1"), build_btn("2"), build_btn("3"),
                                     build_btn("+", ft.Colors.ORANGE_800)]),
                    ft.Row(controls=[build_btn("0"), build_btn("."), build_btn("=", ft.Colors.GREEN_700)]),
                ],
                spacing=8
            ),
            padding=12
        )
    )


if __name__ == "__main__":
    ft.run(main)
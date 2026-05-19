# core/engine.py
import re


class CalculatorEngine:
    def calculate_expression(self, expression: str) -> float:
        expression = expression.strip()
        if not expression or expression == "Error":
            return 0.0


        # Security check: Whitelist safe characters
        allowed_chars = "0123456789+-*/.() %"
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Invalid characters detected.")

        # FEATURE 1: Auto-Closing Parentheses Guardrail
        open_brackets = expression.count("(")
        close_brackets = expression.count(")")
        if open_brackets > close_brackets:
            expression += ")" * (open_brackets - close_brackets)

        # FEATURE 2: Real-World Percentage Engine
        # Context A: Markup/Discount context (e.g., "500 + 10%" or "100 - 20%")
        markup_pattern = r"(.+?)([\+\-])\s*([0-9.]+)\s*%"
        while re.search(markup_pattern, expression):
            match = re.search(markup_pattern, expression)
            base_part = match.group(1)
            operator = match.group(2)
            percentage_val = match.group(3)

            try:
                # Resolve the value of the expression leading up to the percentage calculation
                base_evaluated = eval(base_part)
                parsed_percentage = (float(base_evaluated) * float(percentage_val)) / 100
                expression = expression.replace(match.group(0), f"{base_part}{operator}{parsed_percentage}", 1)
            except Exception:
                raise SyntaxError("Malformed percentage context.")

        # Context B: Standard scale modifier context (e.g., "500 * 10%" or "50 / 2%")
        standard_pct_pattern = r"([0-9.]+)\s*%"
        while re.search(standard_pct_pattern, expression):
            match = re.search(standard_pct_pattern, expression)
            val = match.group(1)
            expression = expression.replace(match.group(0), f"({val}/100)", 1)

        # FEATURE 3: Implied Operand Execution (e.g., trailing "45 +")
        operators = ['+', '-', '*', '/']
        if expression[-1] in operators:
            last_op = expression[-1]
            base_expression = expression[:-1].strip()
            try:
                running_total = eval(base_expression)
                if isinstance(running_total, float) and running_total.is_integer():
                    running_total = int(running_total)
                expression = f"{base_expression}{last_op}{running_total}"
            except Exception:
                raise SyntaxError("Malformed implied expression.")

        # Final evaluation compilation
        try:
            result = eval(expression)
            return float(result)
        except Exception:
            raise SyntaxError("Compilation parsing error.")
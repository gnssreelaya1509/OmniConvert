# core/engine.py

class CalculatorEngine:
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def calculate_expression(self, expression: str) -> float:
        allowed_chars = "0123456789+-*/.() "
        if not all(char in allowed_chars for char in expression):
            raise ValueError("Invalid characters detected.")
        try:
            result = eval(expression)
            return float(result)
        except Exception:
            raise SyntaxError("Malformed expression.")
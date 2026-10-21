from typing import Any, Union, List, Dict
from .ast import IntegralNumber


class ExpressionVisitor:
    """Visitor class to evaluate constant expressions."""

    def __init__(self, variables: Dict[str, Any] = None):
        """Initialize visitor with optional variable bindings."""
        self.variables = variables or {}

    def visit(self, node) -> Any:
        """Generic visit method that dispatches to specific visit methods."""
        # Handle primitive types directly
        if isinstance(node, (int, float, str, bool)):
            return node

        # Handle lists (for array expressions)
        if isinstance(node, list):
            return [self.visit(item) for item in node]

        # Handle IntegralNumber directly
        if isinstance(node, IntegralNumber):
            return self.visit_IntegralNumber(node)

        # Dispatch to specific visit method based on node type/operation
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, None)
        if method is None:
            raise ValueError(f"No visit method for {type(node).__name__}")
        return method(node)

    def visit_BinaryOp(self, node) -> Union[int, float, bool]:
        """Visit binary operator nodes."""
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op in ("*", "/", "+", "-", "%", "**"):
            # Arithmetic operations
            return eval(f"{left} {node.op} {right}")
        elif node.op in ("&", "|", "^", ">>", "<<"):
            # Bitwise operations
            return eval(f"{left} {node.op} {right}")
        elif node.op in ("&&", "||", "==", "!=", "<", ">", "<=", ">="):
            # Logical operations
            return eval(f"{left} {node.op} {right}")
        else:
            raise ValueError(f"Unknown binary operator: {node.op}")

    def visit_UnaryOp(self, node) -> Union[int, float, bool]:
        """Visit unary operator nodes."""
        value = self.visit(node.operand)

        if node.op == "+":
            return +value
        elif node.op == "-":
            return -value
        elif node.op == "~":
            return ~value
        elif node.op == "!":
            return not value
        else:
            raise ValueError(f"Unknown unary operator: {node.op}")

    def visit_Identifier(self, node) -> Any:
        """Visit identifier nodes."""
        if node.name not in self.variables:
            raise ValueError(f"Undefined variable: {node.name}")
        return self.variables[node.name]

    def visit_Conditional(self, node) -> Any:
        """Visit ternary conditional expressions."""
        condition = self.visit(node.condition)
        return self.visit(node.true_expr) if condition else self.visit(node.false_expr)

    def visit_Inside(self, node) -> bool:
        """Visit inside operator expressions."""
        value = self.visit(node.value)
        ranges = self.visit(node.ranges)

        for range_item in ranges:
            if isinstance(range_item, (list, tuple)):
                # Handle range [start:end]
                start, end = range_item
                if start <= value <= end:
                    return True
            else:
                # Handle single value
                if value == range_item:
                    return True
        return False

    def visit_Cast(self, node) -> Union[int, float]:
        """Visit type casting expressions."""
        value = self.visit(node.value)
        if node.type_name in ("int", "bit", "byte", "shortint", "longint"):
            return int(value)
        elif node.type_name in ("real", "shortreal"):
            return float(value)
        else:
            raise ValueError(f"Unsupported cast type: {node.type_name}")

    def visit_MathFunction(self, node) -> float:
        """Visit math function calls."""
        import math

        args = [self.visit(arg) for arg in node.args]

        try:
            if node.name.startswith("$"):
                func_name = node.name[1:]  # Remove $ prefix
            else:
                func_name = node.name

            if hasattr(math, func_name):
                return getattr(math, func_name)(*args)
            else:
                raise ValueError(f"Unknown math function: {node.name}")
        except Exception as e:
            raise ValueError(f"Error evaluating math function {node.name}: {str(e)}")

    def visit_IntegralNumber(self, node: IntegralNumber) -> int:
        """Visit integral number nodes."""
        if node.size is not None:
            # Apply size constraint
            mask = (1 << node.size) - 1
            value = node.value & mask

            # Handle sign extension if signed
            if node.signed and (value & (1 << (node.size - 1))):
                value |= ~mask

            return value
        return node.value

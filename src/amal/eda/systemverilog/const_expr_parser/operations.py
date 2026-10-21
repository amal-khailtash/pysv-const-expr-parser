from dataclasses import dataclass, field
import functools
import math
import operator


@dataclass
class OperationMap:
    """Operation map for SystemVerilog constant expressions."""

    # Unary operators
    uniary_op: dict = field(
        default_factory=lambda: {
            "+": lambda x: x,
            "-": operator.neg,
            "!": operator.not_,
            "~": operator.invert,
            "&": lambda x: functools.reduce(operator.and_, [int(i) for i in f"{x:b}"], 1),
            "|": lambda x: functools.reduce(operator.or_, [int(i) for i in f"{x:b}"], 0),
            "^": lambda x: functools.reduce(operator.or_, [int(i) for i in f"{x:b}"], 0),
            "~&": lambda x: operator.invert(functools.reduce(operator.and_, [int(i) for i in f"{x:b}"], 1)),
            "~|": lambda x: operator.invert(functools.reduce(operator.or_, [int(i) for i in f"{x:b}"], 0)),
            "~^": lambda x: operator.invert(functools.reduce(operator.xor, [int(i) for i in f"{x:b}"], 0)),
            "^~": lambda x: operator.invert(functools.reduce(operator.xor, [int(i) for i in f"{x:b}"], 0)),
        }
    )

    # Binary operators
    binary_op: dict = field(
        default_factory=lambda: {
            "**": operator.pow,
            "*": operator.mul,
            "/": operator.truediv,
            "%": operator.mod,
            "+": operator.add,
            "-": operator.sub,
            "<<": operator.lshift,  # Logical shift-left
            ">>": lambda left, right: left >> right if left >= 0 else -(-left >> right),  # Logical shift-right
            "<<<": operator.lshift,  # Arthmetic shift-left
            ">>>": operator.rshift,  # Arthmetic shift-right
        }
    )

    # Comparison operators
    comparison_op: dict = field(
        default_factory=lambda: {
            "<": operator.lt,
            "<=": operator.le,
            "==": operator.eq,
            "!=": operator.ne,
            ">": operator.gt,
            ">=": operator.ge,
        }
    )

    # Bitwise logical operators
    bitwise_logical_op: dict = field(
        default_factory=lambda: {
            "&": operator.and_,
            "^": operator.xor,
            "~^": lambda left, right: operator.invert(operator.xor(left, right)),
            "^~": lambda left, right: operator.invert(operator.xor(left, right)),
            "|": operator.or_,
            "&&": lambda left, right: left and right,
            "||": lambda left, right: left or right,
        }
    )

    # Math functions
    math_functions: dict = field(
        default_factory=lambda: {
            # Integer Math Functions
            "$clog2": lambda x: int(math.ceil(math.log(x, 2))),
            # Real Math Functions
            "$acos": math.acos,
            "$acosh": math.acosh,
            "$asin": math.asin,
            "$asinh": math.asinh,
            "$atan": math.atan,
            "$atan2": math.atan2,
            "$atanh": math.atanh,
            "$ceil": math.ceil,
            "$cos": math.cos,
            "$cosh": math.cosh,
            "$exp": math.exp,
            "$floor": math.floor,
            "$hypot": math.hypot,
            "$ln": lambda x: math.log(x, math.e),
            "$log10": math.log10,
            "$pow": math.pow,
            "$sin": math.sin,
            "$sinh": math.sinh,
            "$sqrt": math.sqrt,
            "$tan": math.tan,
            "$tanh": math.tanh,
        }
    )


# UNARY_OP = {
#     "+":  lambda x: x,
#     "-":  operator.neg,
#     "!":  operator.not_,
#     "~":  operator.invert,
#     "&":  lambda x: functools.reduce(                operator.and_, [int(i) for i in f"{x:b}"], 1),
#     "|":  lambda x: functools.reduce(                operator.or_,  [int(i) for i in f"{x:b}"], 0),
#     "^":  lambda x: functools.reduce(                operator.or_,  [int(i) for i in f"{x:b}"], 0),
#     "~&": lambda x: operator.invert(functools.reduce(operator.and_, [int(i) for i in f"{x:b}"], 1)),
#     "~|": lambda x: operator.invert(functools.reduce(operator.or_,  [int(i) for i in f"{x:b}"], 0)),
#     "~^": lambda x: operator.invert(functools.reduce(operator.xor,  [int(i) for i in f"{x:b}"], 0)),
#     "^~": lambda x: operator.invert(functools.reduce(operator.xor,  [int(i) for i in f"{x:b}"], 0)),
# }

# BINARY_OP = {
#     "**":  operator.pow,
#     "*":   operator.mul,
#     "/":   operator.truediv,
#     "%":   operator.mod,
#     "+":   operator.add,
#     "-":   operator.sub,
#     "<<":  operator.lshift,                                                        # Logical shift-left
#     ">>":  lambda left, right: left >> right if left >= 0 else -(-left >> right),  # Logical shift-right
#     "<<<": operator.lshift,                                                        # Arthmetic shift-left
#     ">>>": operator.rshift,                                                        # Arthmetic shift-right
# }

# COMPARISON_OP = {
#     "<":  operator.lt,
#     "<=": operator.le,
#     "==": operator.eq,
#     "!=": operator.ne,
#     ">":  operator.gt,
#     ">=": operator.ge,
# }

# BITWISE_LOGICAL_OP = {
#     "&":  operator.and_,
#     "^":  operator.xor,
#     "~^": lambda left, right: operator.invert(operator.xor(left, right)),
#     "^~": lambda left, right: operator.invert(operator.xor(left, right)),
#     "|":  operator.or_,
#     "&&": lambda left, right: left and right,
#     "||": lambda left, right: left or right,
# }

# MATH_FUNCTIONS = {
#     # Integer Math Functions
#     "$clog2": lambda x: int(math.ceil(math.log(x, 2))),
#     # Real Math Functions
#     "$acos":  math.acos,
#     "$acosh": math.acosh,
#     "$asin":  math.asin,
#     "$asinh": math.asinh,
#     "$atan":  math.atan,
#     "$atan2": math.atan2,
#     "$atanh": math.atanh,
#     "$ceil":  math.ceil,
#     "$cos":   math.cos,
#     "$cosh":  math.cosh,
#     "$exp":   math.exp,
#     "$floor": math.floor,
#     "$hypot": math.hypot,
#     "$ln":    lambda x: math.log(x, math.e),
#     "$log10": math.log10,
#     "$pow":   math.pow,
#     "$sin":   math.sin,
#     "$sinh":  math.sinh,
#     "$sqrt":  math.sqrt,
#     "$tan":   math.tan,
#     "$tanh":  math.tanh,
# }

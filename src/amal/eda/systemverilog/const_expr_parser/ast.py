from dataclasses import dataclass
from typing import Optional


class Node:
    """Base class for AST nodes."""

    def __init__(self, line: int, column: int) -> None:
        """Initialize node with line and column information."""
        self.line = line
        self.column = column

    def visit(self, visitor):
        """Dispatch to specific visitor method based on node type."""
        try:
            func = getattr(visitor, f"visit_{self.__class__.__name__}")
            return func(self)
        except AttributeError:
            print(f"Visitor {visitor.__class__.__name__} does not have visit_{self.__class__.__name__} implemented")


@dataclass
class IntegralNumber:
    """Represents a SystemVerilog integral number with size information."""

    value: int
    size: Optional[int] = None
    signed: bool = False

    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

    def __repr__(self):
        size_str = f"{self.size}'" if self.size is not None else ""
        signed_str = "s" if self.signed else ""
        return f"{size_str}{signed_str}d{self.value}"


class Invalid(Node):
    pass


class IntegerLiteral(Node):
    pass


class RealLiteral(Node):
    pass


class TimeLiteral(Node):
    pass


class UnbasedUnsizedIntegerLiteral(Node):
    pass


class StringLiteral(Node):
    pass


class UnaryOp(Node):
    pass


class BinaryOp(Node):
    pass


class ConditionalOp(Node):
    pass


class Inside(Node):
    pass


class Assignment(Node):
    pass


class Concatenation(Node):
    pass


class Replication(Node):
    pass


class Streaming(Node):
    pass


class ElementSelect(Node):
    pass


class RangeSelect(Node):
    pass


class MemberAccess(Node):
    pass


# class Conversion(Node):
#     pass


# class DataType(Node):
#     pass


# class TypeReference(Node):
#     pass


class SimpleAssignmentPattern(Node):
    pass


class StructuredAssignmentPattern(Node):
    pass


class ReplicatedAssignmentPattern(Node):
    pass


class EmptyArgument(Node):
    pass


class ValueRange(Node):
    pass


class Dist(Node):
    pass


class NewArray(Node):
    pass

"""
Pytest tests for SystemVerilog expression parsing using pyslang.

Tests use parametrized fixtures containing expressions from tests/tests.sv.
Each fixture is organized by IEEE 1800 SystemVerilog LRM section numbers.

Coverage includes:
- Arithmetic operators: +, -, *, /, %, **
- Bitwise operators: &, |, ^, ~
- Shift operators: <<, >>, <<<, >>>
- Comparison operators: ==, !=, <, >, <=, >=
- Logical operators: &&, ||, !
- Conditional operator: ? :
- Concatenation: {a, b}
- Replication: {N{expr}}
- Unary operators: +, -, ~, reduction &, |, ^
- System functions: $clog2, $bits
- Assignment patterns: '{...}
- Inside operator: inside {...}
- Complex combined expressions
- Integer literals (decimal, binary, hex, octal)
"""

import pytest

ScriptSession = pytest.importorskip("pyslang").ScriptSession
pytestmark = pytest.mark.slang


# ============================================================================
# Core fixtures
# ============================================================================

@pytest.fixture
def session():
    """Create a ScriptSession instance for tests."""
    return ScriptSession()


@pytest.fixture
def eval_int(session):
    """Fixture that evaluates expression and returns Python int."""
    def _eval(expr: str) -> int:
        result = session.eval(expr)
        return int(result.value)
    return _eval


@pytest.fixture
def eval_bool(session):
    """Fixture that evaluates expression and returns Python bool."""
    def _eval(expr: str) -> bool:
        result = session.eval(expr)
        return result.isTrue()
    return _eval


@pytest.fixture
def eval_expr(session):
    """Fixture that evaluates expression and returns ConstantValue."""
    def _eval(expr: str):
        return session.eval(expr)
    return _eval


# ============================================================================
# Test data fixtures - Each contains (expression, expected_result, description)
# Organized by IEEE 1800 SystemVerilog LRM sections
# ============================================================================

# Arithmetic Operators
@pytest.fixture(params=[
    ("5 + 3", 8),
    ("5'b0101 + 4'b1100", 17),
    ("16", 16),
    ("10 + 5", 15),
    ("20 - 8", 12),
    ("4 * 7", 28),
    ("100 / 3", 33),
    ("17 % 5", 2),
    ("2 ** 8", 256),
    ("10 ** 2", 100),
    ("3 * 5 + 2", 17),
    ("10 - 2 * 3", 4),
    ("(2 + 3) ** 2", 25),
])
def arithmetic_expr(request):
    """Fixture for arithmetic expressions."""
    return request.param


# Bitwise Operators
@pytest.fixture(params=[
    ("8'hFF & 8'h0F", 0x0F),
    ("8'hAA | 8'h55", 0xFF),
    ("8'hAA ^ 8'h55", 0xFF),
    ("~8'hF0", 0x0F),
    ("4'b1100 & 4'b1010", 0b1000),
    ("4'b1100 | 4'b1010", 0b1110),
    ("4'b1100 ^ 4'b1010", 0b0110),
])
def bitwise_expr(request):
    """Fixture for bitwise expressions."""
    return request.param


# 11.4.10: Shift Operators
@pytest.fixture(params=[
    ("8'h01 << 4", 0x10),
    ("8'hF0 >> 2", 0x3C),
    ("8'd8 <<< 3", 64),
    ("8'd8 >>> 3", 1),
])
def shift_expr(request):
    """Fixture for shift expressions."""
    return request.param


# 11.4.5: Equality Operators
# 11.4.6: Relational Operators
@pytest.fixture(params=[
    ("10 == 10", True),
    ("10 == 5", False),
    ("10 != 5", True),
    ("10 != 10", False),
    ("10 > 5", True),
    ("5 > 10", False),
    ("10 < 5", False),
    ("5 < 10", True),
    ("10 >= 5", True),
    ("10 >= 10", True),
    ("5 >= 10", False),
    ("10 <= 5", False),
    ("10 <= 10", True),
    ("5 <= 10", True),
])
def comparison_expr(request):
    """Fixture for comparison expressions."""
    return request.param


# 11.4.7: Logical Operators
@pytest.fixture(params=[
    ("1 && 1", True),
    ("1 && 0", False),
    ("0 && 1", False),
    ("0 || 1", True),
    ("1 || 0", True),
    ("0 || 0", False),
    ("!0", True),
    ("!1", False),
])
def logical_expr(request):
    """Fixture for logical expressions."""
    return request.param


# 11.4.11: Conditional Operator
@pytest.fixture(params=[
    ("(1) ? 0 : 1", 0),
    ("(0) ? 0 : 1", 1),
    ("(12 > 5) ? 11 : 13", 11),
    ("(5 > 12) ? 11 : 13", 13),
    ("1 ? 100 : 200", 100),
])
def conditional_expr(request):
    """Fixture for conditional (ternary) expressions."""
    return request.param


# 11.4.12: Concatenation Operators
@pytest.fixture(params=[
    ("{4'b1010, 4'b0101}", 0b10100101),
    ("{8'b10101100, 8'b01010011}", 0b1010110001010011),
    ("{8'h89, 8'h12}", 0x8912),
    ("{4'h3, 4'hA}", 0x3A),
    ("{2'b11, 2'b00, 2'b11}", 0b110011),
])
def concat_expr(request):
    """Fixture for concatenation expressions."""
    return request.param


# System Functions
@pytest.fixture(params=[
    ("$clog2(16)", 4),
    ("$clog2(256)", 8),
    ("$clog2(1024)", 10),
    ("$clog2(17)", 5),
    ("$clog2(100)", 7),
    ("$bits(8'hFF)", 8),
    ("$bits(16'hABCD)", 16),
])
def math_func_expr(request):
    """Fixture for math function expressions."""
    return request.param


# 11.4.2: Unary Operators (including reduction)
@pytest.fixture(params=[
    ("+5", 5),
    ("-10", -10),
    ("~8'b00001111", 0xF0),
    ("&8'b11111111", 1),
    ("&8'b11111110", 0),
    ("|8'b00000000", 0),
    ("|8'b00000001", 1),
    ("^8'b10101010", 0),
    ("^8'b10101011", 1),
])
def unary_expr(request):
    """Fixture for unary operator expressions."""
    return request.param


# 11.4.12.1: Replication Operator
@pytest.fixture(params=[
    ("{2{4'b1010}}", 0b10101010),
    ("{3{2'b11}}", 0b111111),
    ("{4{1'b1}}", 0b1111),
])
def replication_expr(request):
    """Fixture for replication operator expressions."""
    return request.param


# Integer Literals
@pytest.fixture(params=[
    ("35'd123498234", 123498234),
    ("16", 16),
    ("999999999", 999999999),
    ("-5", -5),
    ("-100", -100),
])
def literal_expr(request):
    """Fixture for integer literal expressions."""
    return request.param


# Complex/Combined Expressions
@pytest.fixture(params=[
    ("(10 + 5) * 2", 30),
    ("8'hFF >> 2 | 8'h0F", 0x3F),
    ("2 ** $clog2(100)", 128),
    ("(5 + 3) * (10 - 2)", 64),
    ("100 / (2 + 3)", 20),
    ("(8'hF0 & 8'hAA) | 8'h05", 0xA5),
    ("{2{4'b1010}} & 8'hF0", 0xA0),
])
def complex_expr(request):
    """Fixture for complex combined expressions."""
    return request.param


# 11.4.13: Inside Operator (Set Membership)
@pytest.fixture(params=[
    ("(3 inside {2, 3, 4, 5})", True),
    ("(1 inside {2, 3, 4, 5})", False),
])
def inside_expr(request):
    """Fixture for 'inside' operator expressions."""
    return request.param


# Assignment Patterns
@pytest.fixture(params=[
    "int'{42, -39}",
    "int'{999, '{1, 0}}",
    "int'{1, 2, 3}",
    "int'{2 {42}}",
    "int'{2 {2}}",
    "int'{2 {1, 2}}",
    "int'{3 {2}}",
])
def assignment_pattern_expr(request):
    """Fixture for assignment pattern expressions."""
    return request.param


# ============================================================================
# Parametrized tests
# ============================================================================

def test_arithmetic_expressions(eval_int, arithmetic_expr):
    """Test arithmetic expressions."""
    expr, expected = arithmetic_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_bitwise_expressions(eval_int, bitwise_expr):
    """Test bitwise expressions."""
    expr, expected = bitwise_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_shift_expressions(eval_int, shift_expr):
    """Test shift expressions."""
    expr, expected = shift_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_comparison_expressions(eval_bool, comparison_expr):
    """Test comparison expressions."""
    expr, expected = comparison_expr
    result = eval_bool(expr)
    assert result == expected, f"Failed: {expr}"


def test_logical_expressions(eval_bool, logical_expr):
    """Test logical expressions."""
    expr, expected = logical_expr
    result = eval_bool(expr)
    assert result == expected, f"Failed: {expr}"


def test_conditional_expressions(eval_int, conditional_expr):
    """Test conditional (ternary) expressions."""
    expr, expected = conditional_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_concatenation_expressions(eval_int, concat_expr):
    """Test concatenation expressions."""
    expr, expected = concat_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_math_function_expressions(eval_int, math_func_expr):
    """Test math function expressions."""
    expr, expected = math_func_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_complex_expressions(eval_int, complex_expr):
    """Test complex combined expressions."""
    expr, expected = complex_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_inside_expressions(eval_bool, inside_expr):
    """Test 'inside' operator expressions."""
    expr, expected = inside_expr
    result = eval_bool(expr)
    assert result == expected, f"Failed: {expr}"


def test_assignment_pattern_expressions(eval_expr, assignment_pattern_expr):
    """Test assignment pattern expressions."""
    expr = assignment_pattern_expr
    result = eval_expr(expr)
    assert result is not None, f"Failed: {expr}"


def test_unary_expressions(eval_int, unary_expr):
    """Test unary operator expressions."""
    expr, expected = unary_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_replication_expressions(eval_int, replication_expr):
    """Test replication operator expressions."""
    expr, expected = replication_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


def test_literal_expressions(eval_int, literal_expr):
    """Test integer literal expressions."""
    expr, expected = literal_expr
    result = eval_int(expr)
    assert result == expected, f"Failed: {expr}"


if __name__ == "__main__":  # pragma: no cover
    # Run pytest when executed directly
    pytest.main([__file__, "-v", "-p", "no:terminalprogress"])

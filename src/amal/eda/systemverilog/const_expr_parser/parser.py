# pylint: disable=too-many-lines

# import html
# html.unescape("Suzy &amp; John")
# # "Suzy & John"
#
# html.unescape("&quot;")
# # '"'

import math
import re

from sly import Parser
from sly.lex import Token
from sly.yacc import Production  # , YaccError

# from bit_vector import BitVector

from .lexer import ConstantExpressionLexer
from .exceptions import ConstantExpressionParseError
from .operations import OperationMap
from .ast import IntegralNumber

# get rid of pylint error
_ = lambda *args, **kwargs: None  # noqa: E731


# def _rule(s):
#     return [x.strip() for x in s.split("|")]


#   Exactly_One_Attribute : STRING | NUMBER
#   Zero_Or_More_Attributes : Zero_Or_More_Attributes Attribute | empty
#   One_Or_More_Attributes: One_Or_More_Attributes Attribute | Attribute
#   Attribute_opt : empty | Attribute
# Right recursion
#   Zero_Or_More_Attributes : Attribute Zero_Or_More_Attributes | empty


# pylint: disable=too-many-public-methods
class ConstantExpressionParser(Parser):
    """SystemVerilog Constant Expression Parser."""

    # debugfile = "expression_parser.txt"

    tokens = ConstantExpressionLexer.tokens

    start = "constant_expression"

    # Expression Precedence
    # Reference: http://hp.vector.co.jp/authors/VA016670/verilog/index.html
    precedence = (
        # ("nonassoc", "LT", "GT", "LE", "GE"),  # Nonassociative operators                              # 14
        # <- Weak
        ("right", "IMPL", "EQUIV"),  # 13
        ("right", "COND", "COLON"),  # 12
        ("left", "LOR"),  # 11
        ("left", "LAND"),  # 10
        ("left", "OR"),  # 9
        ("left", "AND", "XOR", "XNOR"),  # 8
        ("left", "EQ", "NE"),  # , "EQL", "NEL"),                                                        # 7
        ("left", "LT", "GT", "LE", "GE", "INSIDE"),  # 6
        # ("left", "INSIDE"),                                                                            # 6
        ("left", "LSHIFT", "RSHIFT", "LSHIFTA", "RSHIFTA"),  # 5
        ("left", "PLUS", "MINUS"),  # 4
        ("left", "TIMES", "DIVIDE", "MOD"),  # 3
        ("left", "POWER"),  # 2
        ("right", "UMINUS", "UPLUS", "ULNOT", "UNOT", "UAND", "UNAND", "UOR", "UNOR", "UXOR", "UXNOR"),  # 1
        # -> Strong
    )

    # precedence = (
    #     ("left", "yP_ANDANDAND"),
    #     ("left", "yMATCHES"),
    #     ("left", "prTAGGED"),
    #     ("left", "prSEQ_CLOCKING"),
    #     ("nonassoc", "yALWAYS", "yS_ALWAYS", "yEVENTUALLY", "yS_EVENTUALLY", "yACCEPT_ON",
    #                  "yREJECT_ON", "ySYNC_ACCEPT_ON", "ySYNC_REJECT_ON"),
    #     ("right", "yP_ORMINUSGT", "yP_OREQGT", "yP_POUNDMINUSPD", "yP_POUNDEQPD"),
    #     ("right", "yUNTIL", "yS_UNTIL", "yUNTIL_WITH", "yS_UNTIL_WITH", "yIMPLIES"),
    #     ("right", "yIFF"),
    #     ("left", "yOR"),
    #     ("left", "yAND"),
    #     ("nonassoc", "yNOT", "yNEXTTIME", "yS_NEXTTIME"),
    #     ("left", "yINTERSECT"),
    #     ("left", "yWITHIN"),
    #     ("right", "yTHROUGHOUT"),
    #     ("left", "prPOUNDPOUND_MULTI"),
    #     ("left", "yP_POUNDPOUND"),
    #     ("left", "yP_BRASTAR", "yP_BRAEQ", "yP_BRAMINUSGT", "yP_BRAPLUSKET"),
    #     ("left", "yPOSEDGE", "yNEGEDGE", "yEDGE"),
    #     ("left", ""{"", ""}""),
    #     ("right", "yP_MINUSGT", "yP_LTMINUSGT"),
    #     ("right", ""?"", "":""),
    #     ("left", "yP_OROR"),
    #     ("left", "yP_ANDAND"),
    #     ("left", ""|"", "yP_NOR"),
    #     ("left", ""^"", "yP_XNOR"),
    #     ("left", ""&"", "yP_NAND"),
    #     ("left", "yP_EQUAL", "yP_NOTEQUAL", "yP_CASEEQUAL", "yP_CASENOTEQUAL", "yP_WILDEQUAL", "yP_WILDNOTEQUAL"),
    #     ("left", "">"", ""<"", "yP_GTE", "yP_LTE", "yP_LTE__IGNORE", "yINSIDE", "yDIST"),
    #     ("left", "yP_SLEFT", "yP_SRIGHT", "yP_SSRIGHT"),
    #     ("left", ""+"", ""-""),
    #     ("left", ""*"", ""/"", ""%""),
    #     ("left", "yP_POW"),
    #     ("left", "prUNARYARITH", "yP_MINUSMINUS", "yP_PLUSPLUS", "prREDUCTION", "prNEGATION"),
    #     ("left", "".""),
    #     ("left", "yP_TICK"),
    #     ("nonassoc", "prLOWER_THAN_ELSE"),
    #     ("nonassoc", "yELSE")
    # )

    # @_("")  # noqa: F821
    # def empty(self, production: Production):
    #     """
    #     Empty grammar rule.
    #     """
    #     pass

    # @_("number", "string_literal")  # noqa: F821
    # @_(*[x.strip() for x in "number | string_literal".split("|")])  # noqa: F821
    # @_(*_rule("number | string_literal"))  # noqa: F821
    # def start_rule(self, production: Production):
    #     """
    #     start_rule ::= number | string_literal
    #     """
    #     return production

    # @staticmethod
    @_("UNBASED_UNSIZED_LITERAL")  # noqa: F821
    # pylint: disable=no-self-use
    def unbased_unsized_literal(self, production: Production):
        """unbased_unsized_literal ::= UNBASED_UNSIZED_LITERAL"""
        return production

    # @staticmethod
    @_("BINARY_NUMBER")  # noqa: F821
    # pylint: disable=no-self-use
    def integral_number(self, production: Production):
        """integral_number ::= binary_number | octal_number | decimal_number | hex_number"""
        number = production.BINARY_NUMBER.replace("_", "")
        parts = number.partition("'")

        num_bits = int(parts[0]) if parts[0] != "" else 32
        signed = "s" in parts[2] or "S" in parts[2]  # noqa: F841 - pylint: disable=unused-variable
        value = re.sub("[sSbB]", "", parts[2])

        # print(f"num_bits: {num_bits}, signed: {signed}, value: {value}")

        # bits = math.ceil(math.log(int(value) + 1, 2))
        # print(f"bits: {bits}")

        value = int(value, 2)
        bits = math.ceil(math.log(value + 1, 2))
        # bits = len(value)

        # if bits > num_bits:
        #     print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
        #     value = BitVector(int(value[-num_bits:], 2), num_bits, signed)
        # else:
        #     value = BitVector(int(value, 2), num_bits, signed)

        # try:
        #     value = BitVector(int(value, 2), num_bits, signed)
        # except Exception as err:
        #     # print(err)
        #     print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
        #     value = BitVector(int(value, 2) & ((1 << num_bits) - 1), num_bits, signed)

        # # print(f"---> {value} ({bits})")
        if bits > num_bits:
            print(f"WARNING: {number} needs {bits} bits! Truncating to {num_bits} bits...")
            value = value & ((1 << num_bits) - 1)

        # print(f"value: {value.as_binary_string()}")
        # print(f"value: {value.as_int():0{num_bits+int(math.ceil((num_bits - 4)/4))}_b}")
        # return value
        # return parts
        # return production
        return IntegralNumber(value=value, size=num_bits, signed=signed)

    # @staticmethod
    @_("OCTAL_NUMBER")  # noqa: F821
    # pylint: disable=no-self-use,function-redefined
    def integral_number(self, production: Production):  # noqa: F811
        """integral_number ::= binary_number | octal_number | decimal_number | hex_number"""
        number = production.OCTAL_NUMBER.replace("_", "")
        parts = number.partition("'")

        # num_bits = int(parts[0])
        # value = int(parts[2][1:], 8)

        num_bits = int(parts[0]) if parts[0] != "" else 32
        signed = "s" in parts[2] or "S" in parts[2]  # noqa: F841 - pylint: disable=unused-variable
        value = re.sub("[sSoO]", "", parts[2])

        # print(f"num_bits: {num_bits}, signed: {signed}, value: {value}")

        value = int(value, 8)
        bits = math.ceil(math.log(value + 1, 2))
        # bits = len(value) * 3

        # if bits > num_bits:
        #     print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
        #     value = BitVector(int(value[-int(math.floor(num_bits // 3)):], 8), num_bits, signed)
        # else:
        #     value = BitVector(int(value, 8), num_bits, signed)

        # try:
        #     value = BitVector(int(value, 8), num_bits, signed)
        # except Exception as err:
        #     # print(err)
        #     print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
        #     value = BitVector(int(value, 8) & ((1 << num_bits) - 1), num_bits, signed)

        # # print(f"---> {value} ({bits})")
        if bits > num_bits:
            print(f"WARNING: {number} needs {bits} bits! Truncating to {num_bits} bits...")
            value = value & ((1 << num_bits) - 1)

        # print(f"value: {value.as_binary_string()}")
        # print(f"value: {value.as_int():0{num_bits+int(math.ceil((num_bits - 4)/4))}_b}")
        # return value
        # return production
        return IntegralNumber(value=value, size=num_bits, signed=signed)

    # @staticmethod
    @_("DECIMAL_NUMBER")  # noqa: F821
    # pylint: disable=no-self-use,function-redefined
    def integral_number(self, production: Production):  # noqa: F811
        """integral_number ::= binary_number | octal_number | decimal_number | hex_number"""
        number = production.DECIMAL_NUMBER.replace("_", "")
        parts = number.partition("'")

        signed = True
        if not parts[1]:
            value = int(number)
            num_bits = 32
            # signed = True
            # value = number
        else:
            # num_bits = int(parts[0])
            # value = int(parts[2][1:])

            num_bits = int(parts[0]) if parts[0] != "" else 32
            signed = "s" in parts[2] or "S" in parts[2]  # noqa: F841 - pylint: disable=unused-variable
            value = re.sub("[sSdD]", "", parts[2])

        value = int(value)
        bits = math.ceil(math.log(value + 1, 2))

        # try:
        #     value = BitVector(int(value), num_bits, signed)
        # except Exception as err:
        #     # print(err)
        #     print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
        #     value = BitVector(int(value) & ((1 << num_bits) - 1), num_bits, signed)

        # print(f"---> {value} ({bits})")
        if bits > num_bits:
            print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
            value = value & ((1 << num_bits) - 1)

        # print(f"value: {value.as_binary_string()}")
        # print(f"value: {value.as_int():0{num_bits+int(math.ceil((num_bits - 4)/4))}_b}")

        # return value
        # return production
        return IntegralNumber(value=value, size=num_bits, signed=signed)

    # @staticmethod
    @_("HEX_NUMBER")  # noqa: F821
    # pylint: disable=no-self-use,function-redefined
    def integral_number(self, production: Production):  # noqa: F811
        """integral_number ::= binary_number | octal_number | decimal_number | hex_number"""
        if "x" in production.HEX_NUMBER.lower():
            value = int(production.HEX_NUMBER, 0)
            return value

        number = production.HEX_NUMBER.replace("_", "")
        parts = number.partition("'")

        # num_bits = int(parts[0])
        # value = int(parts[2][1:], 16)

        num_bits = int(parts[0]) if parts[0] != "" else 32
        signed = "s" in parts[2] or "S" in parts[2]  # noqa: F841 - pylint: disable=unused-variable
        value = re.sub("[sShH]", "", parts[2])

        # print(f"num_bits: {num_bits}, signed: {signed}, value: {value}")

        value = int(value, 16)
        bits = math.ceil(math.log(value + 1, 2))
        # bits = len(value) * 4

        # try:
        #     value = BitVector(int(value, 16), num_bits, signed)
        # except Exception as err:
        #     # print(err)
        #     print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
        #     value = BitVector(int(value, 16) & ((1 << num_bits) - 1), num_bits, signed)

        # print(f"---> {value} ({bits})")
        if bits > num_bits:
            print(f"WARNING: {number} requires {bits} bits! Truncating to {num_bits} bits...")
            value = value & ((1 << num_bits) - 1)

        # print(f"value: {value.as_binary_string()}")
        # print(f"value: {value.as_int():0{num_bits+int(math.ceil((num_bits - 4)/4))}_b}")
        # return value
        # return production
        return IntegralNumber(value=value, size=num_bits, signed=signed)

    # @_("BINARY_NUMBER", "OCTAL_NUMBER", "DECIMAL_NUMBER", "HEX_NUMBER",)
    # def integral_number(self, production: Production):
    #     """
    #     integral_number ::= binary_number | octal_number | decimal_number | hex_number
    #     """
    #     # production.set_lineno(0, production.lineno(1))
    #     return production

    # @staticmethod
    @_("REAL_NUMBER")  # noqa: F821
    # pylint: disable=no-self-use
    def real_number(self, production: Production):
        """real_number ::= REAL_NUMBER"""
        # production.set_lineno(0, production.lineno(1))
        return float(production.REAL_NUMBER.replace("_", ""))

    # @staticmethod
    @_("real_number", "integral_number")  # noqa: F821
    # pylint: disable=no-self-use
    def number(self, production: Production):
        """number ::= integral_number | real_number"""
        # production.set_lineno(0, production.lineno(1))
        return production[0]

    # @staticmethod
    @_("STRING_LITERAL")  # noqa: F821
    # pylint: disable=no-self-use
    def string_literal(self, production: Production):
        """string_literal := STRING_LITERAL"""
        # production.set_lineno(0, production.lineno(1))
        # return ("string_literal", production.STRING_LITERAL[1:-1])  # strip \" and \"
        return production.STRING_LITERAL[1:-1]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.1 Declarations: declaration data types
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # @staticmethod
    @_("simple_type", "constant_primary", "signing")  # noqa: F821
    # pylint: disable=no-self-use
    def casting_type(self, production: Production):
        """casting_type ::= simple_type | constant_primary | signing"""
        return production[0]

    # @staticmethod
    @_("integer_vector_type", "integer_atom_type")  # noqa: F821
    # pylint: disable=no-self-use
    def integer_type(self, production: Production):
        """integer_type ::= integer_vector_type | integer_atom_type"""
        return production[0]

    # @staticmethod
    @_("BYTE", "SHORTINT", "INT", "LONGINT")  # noqa: F821
    # pylint: disable=no-self-use
    def integer_atom_type(self, production: Production):
        """integer_atom_type ::= "byte" | "shortint" | "int" | "longint" """
        return production[0]

    # @staticmethod
    @_("BIT")  # noqa: F821
    # pylint: disable=no-self-use
    def integer_vector_type(self, production: Production):
        """integer_vector_type ::= "bit" """
        return production[0]

    # @staticmethod
    @_("SHORTREAL", "REAL")  # noqa: F821
    # pylint: disable=no-self-use
    def non_integer_type(self, production: Production):
        """non_integer_type ::= "shortreal" | "real" """
        return production[0]

    # @staticmethod
    @_("SIGNED", "UNSIGNED")  # noqa: F821
    # pylint: disable=no-self-use
    def signing(self, production: Production):
        """signing ::= "signed" | "unsigned" """
        return production[0]

    # @staticmethod
    @_("integer_type", "non_integer_type")  # noqa: F821
    # pylint: disable=no-self-use
    def simple_type(self, production: Production):
        """simple_type ::= integer_type | non_integer_type"""
        return production[0]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.2 Behavioral statements: Case statements
    # E.6.2.1 Patterns
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #   Exactly_One_Attribute : STRING | NUMBER
    #   Zero_Or_More_Attributes : Zero_Or_More_Attributes Attribute | empty
    #   One_Or_More_Attributes: One_Or_More_Attributes Attribute | Attribute
    #   Attribute_opt : empty | Attribute
    # Right recursion
    #   Zero_Or_More_Attributes : Attribute Zero_Or_More_Attributes | empty

    # ""{" expression_list_proper "}"
    # ""{" "}"
    #
    # expression_list_proper
    #   : expression_list_proper "," expression
    #   | expression
    #   ;

    # @staticmethod
    @_(  # noqa: F821
        "TICK_BRACKET pattern_list        '}'",
        "TICK_BRACKET pattern_member_list '}'",
        "TICK_BRACKET                     '}'",
    )
    # pylint: disable=no-self-use
    def assignment_pattern(self, production: Production):
        """assignment_pattern
        ::= '"{" pattern_list        "}"
          | '"{" pattern_member_list "}"
          | '"{"                     "}"
        """
        return production

    # @staticmethod
    @_(  # noqa: F821
        "pattern_one",
        "pattern_list COMMA pattern_one",
    )
    # pylint: disable=no-self-use
    def pattern_list(self, production: Production):
        """pattern_list
        ::= pattern_one
          | pattern_list "," pattern_one
        """
        return production

    # @staticmethod
    @_(  # noqa: F821
        "constant_expression",
        "constant_expression '{' args_expr_list '}'",
        # "patternNoExpr",
    )
    # pylint: disable=no-self-use
    def pattern_one(self, production: Production):
        """pattern_one
        ::= constant_expression
          | constant_expression "{" args_expr_list "}"
        """
        return production

    # @staticmethod
    @_(  # noqa: F821
        "constant_expression",
        "args_expr_list COMMA constant_expression",
    )
    # pylint: disable=no-self-use
    def args_expr_list(self, production: Production):
        """args_expr_list
        ::= constant_expression
          | args_expr_list "," constant_expression
        """
        return production

    # patternNoExpr:
    #     "." id
    #   |  yP_DOTSTAR
    #   |  yTAGGED id patternNoExpr

    # @staticmethod
    @_(  # noqa: F821
        "array_pattern_key COLON constant_expression",
        # "array_pattern_key COLON patternNoExpr",
        "pattern_member_list COMMA array_pattern_key COLON constant_expression",
        # "pattern_member_list COMMA array_pattern_key COLON patternNoExpr",
    )
    # pylint: disable=no-self-use
    def pattern_member_list(self, production: Production):
        """pattern_member_list
        ::= array_pattern_key ":" constant_expression
          | pattern_member_list "," array_pattern_key ":" constant_expression
        """
        return production

    # @_(  # noqa: F821
    #     ""\"" "{" constant_expression__list "}"",
    #     ""\"" "{" array_pattern_key__constant_expression__list "}"",
    #     ""\"" "{" constant_expression "{" constant_expression__list "}" "}"",
    # )
    # def assignment_pattern(self, production: Production):
    #     """
    #   assignment_pattern
    #     ::= ""{"                         constant_expression {","                       constant_expression} "}"
    #       | ""{" array_pattern_key   ":" constant_expression {"," array_pattern_key ":" constant_expression} "}"
    #       | ""{" constant_expression "{" constant_expression {","                       constant_expression} "}" "}"
    #
    #     """
    #     return production

    # @_(  # noqa: F821
    #     "                              constant_expression",
    #     "constant_expression__list "," constant_expression",
    # )
    # def constant_expression__list(self, production: Production):
    #     """
    #     constant_expression__list = constant_expression { "," constant_expression }
    #     """
    #     return production

    # @_(  # noqa: F821
    #     "                                                 array_pattern_key ":" constant_expression",
    #     "array_pattern_key__constant_expression__list "," array_pattern_key ":" constant_expression",
    # )
    # def array_pattern_key__constant_expression__list(self, production: Production):
    #     """
    #     array_pattern_key__constant_expression__list :=
    #         array_pattern_key ":" constant_expression { "," array_pattern_key ":" constant_expression }
    #     """
    #     return production

    # @staticmethod
    @_("constant_expression", "assignment_pattern_key")  # noqa: F821
    # pylint: disable=no-self-use
    def array_pattern_key(self, production: Production):
        """array_pattern_key ::= constant_expression | assignment_pattern_key"""
        return production[0]

    # @staticmethod
    @_("simple_type")  # noqa: F821
    # pylint: disable=no-self-use
    def assignment_pattern_key(self, production: Production):
        """assignment_pattern_key ::= simple_type"""
        return production[0]

    # @staticmethod
    @_(  # noqa: F821
        "assignment_pattern",
        "integer_atom_type assignment_pattern",  # reduce/reduce conflicts
        # "assignment_pattern_expression_type assignment_pattern",
    )
    # pylint: disable=no-self-use
    def assignment_pattern_expression(self, production: Production):
        """assignment_pattern_expression ::= [ assignment_pattern_expression_type ] assignment_pattern"""
        return production

    # @staticmethod
    # @_("integer_atom_type")
    # # pylint: disable=no-self-use
    # def assignment_pattern_expression_type(self, production: Production):
    #     """
    #     assignment_pattern_expression_type ::= integer_atom_type
    #     """
    #     return production

    # @staticmethod
    @_("assignment_pattern_expression")  # noqa: F821
    # pylint: disable=invalid-name,no-self-use
    def constant_assignment_pattern_expression(self, production: Production):
        """constant_assignment_pattern_expression ::= assignment_pattern_expression"""
        return production[0]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.2.2 Covergroup declarations
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # open_range_list ::= open_value_range { "," open_value_range }
    # @staticmethod
    @_("open_value_range")  # noqa: F821
    # pylint: disable=no-self-use
    def open_range_list(self, production: Production):
        """open_range_list ::= open_value_range"""
        if isinstance(production.open_value_range, list):
            return production.open_value_range

        return [production.open_value_range]

    # @staticmethod
    @_("open_range_list COMMA open_value_range")  # noqa: F821
    # pylint: disable=no-self-use,function-redefined
    def open_range_list(self, production: Production):  # noqa: F811
        """open_range_list ::= open_range_list "," open_value_range"""
        if isinstance(production.open_value_range, list):
            return production.open_range_list + production.open_value_range

        return production.open_range_list + [production.open_value_range]

    # @staticmethod
    @_("value_range")  # noqa: F821
    # pylint: disable=no-self-use
    def open_value_range(self, production: Production):
        """open_value_range ::= value_range"""
        return production.value_range

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.3 Expressions
    # E.6.3.1 Concatenations
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # @staticmethod
    @_(  # noqa: F821
        "'{' constant_expression constant_expression__cont",
        # "'{' constant_expression                           '}'",
        # "'{' constant_expression COMMA constant_expression '}'",
    )
    # pylint: disable=no-self-use
    def constant_concatenation(self, production: Production):
        """constant_concatenation ::= "{" constant_expression { "," constant_expression } "}" """
        return production

    # @staticmethod
    @_(  # noqa: F821
        "'}'", "COMMA constant_expression constant_expression__cont"
    )
    # pylint: disable=no-self-use
    def constant_expression__cont(self, production: Production):
        """constant_expression__cont
        ::= "}"
          | COMMA constant_expression constant_expression__cont
        """
        return production

    # @staticmethod
    @_("'{' constant_expression constant_concatenation '}'")  # noqa: F821
    # pylint: disable=no-self-use
    def constant_multiple_concatenation(self, production: Production):
        """constant_multiple_concatenation ::= "{" constant_expression constant_concatenation "}" """
        return production

    # @staticmethod
    @_(  # noqa: F821
        "'{' stream_operator            constant_stream_concatenation '}'",
        "'{' stream_operator slice_size constant_stream_concatenation '}'",
    )
    # pylint: disable=no-self-use
    def constant_streaming_expression(self, production: Production):
        """constant_streaming_expression ::= "{" stream_operator [ slice_size ] constant_stream_concatenation "}" """
        return production

    # @staticmethod
    @_("RSHIFT", "LSHIFT")  # noqa: F821
    # pylint: disable=no-self-use
    def stream_operator(self, production: Production):
        """stream_operator ::= ">>" | "<<" """
        return production

    # @staticmethod
    @_("simple_type", "constant_expression")  # noqa: F821
    # pylint: disable=no-self-use
    def slice_size(self, production: Production):
        """slice_size ::= simple_type | constant_expression"""
        return production

    # @staticmethod
    @_(  # noqa: F821
        "'{' constant_stream_expression__list '}'",
        # ""{" constant_stream_expression "}"",
        # ""{" constant_stream_concatenation COMMA constant_stream_expression "}"",
    )
    # pylint: disable=no-self-use
    def constant_stream_concatenation(self, production: Production):
        """constant_stream_concatenation ::= "{" constant_stream_expression { "," constant_stream_expression } "}" """
        return production

    # pylint: disable=invalid-name
    @_(  # noqa: F821
        "                                       constant_stream_expression",
        "constant_stream_expression__list COMMA constant_stream_expression",
    )
    # pylint: disable=no-self-use
    def constant_stream_expression__list(self, production: Production):
        """
        constant_stream_expression__list ::= constant_stream_expression { "," constant_stream_expression }
        """
        return production

    @_(  # noqa: F821
        # "constant_expression",  # reduce/reduce
        "constant_expression WITH '[' constant_array_range_expression ']'",
    )
    # pylint: disable=no-self-use
    def constant_stream_expression(self, production: Production):
        """
        constant_stream_expression ::= constant_expression [ "with" "[" constant_array_range_expression "]" ]
        """
        return production

    @_(  # noqa: F821
        "constant_expression",
        "constant_expression COLON      constant_expression",
        "constant_expression PLUSCOLON  constant_expression",
        "constant_expression MINUSCOLON constant_expression",
    )
    # pylint: disable=no-self-use
    def constant_array_range_expression(self, production: Production):
        """
        constant_array_range_expression ::= constant_expression
                                          | constant_expression  ":" constant_expression
                                          | constant_expression "+:" constant_expression
                                          | constant_expression "-:" constant_expression
        """
        return production

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.3.2 Subroutine calls
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @_(  # noqa: F821
        "math_function_identifier '(' list_of_arguments ')'",
        # "math_function_identifier",
        # "math_function_identifier "(" list_of_arguments ")"",
    )
    # pylint: disable=no-self-use
    def math_function_call(self, production: Production):
        """
        math_function_call ::= math_function_identifier [ "(" list_of_arguments ")" ]
        """
        n_arguments = len(production.list_of_arguments)

        if production.math_function_identifier not in ("$atan2", "$hypot", "$pow"):
            if n_arguments != 1:
                print(f"ERROR: Expected one argument, but got {n_arguments}!")
                print(f"{production.lineno:4}:{production.index:4}: ")
                return 0.0
        else:
            if n_arguments != 2:
                print(f"ERROR: Expected one argument, but got {n_arguments}!")
                print(f"{production.lineno:4}:{production.index:4}: ")
                return 0.0

        result = 0.0
        try:
            result = self.operations.math_functions[production.math_function_identifier](*production.list_of_arguments)
        except ValueError as err:
            print(f"Illegal operation: {err}")

        return result

    @_(  # noqa: F821
        # "",
        "constant_expression",
        # "list_of_arguments COMMA",
        "list_of_arguments COMMA constant_expression",
    )
    # pylint: disable=no-self-use
    def list_of_arguments(self, production: Production):
        """
        list_of_arguments ::= [ constant_expression ] { "," [ constant_expression ] }
        """
        if len(production) == 1:
            return (production.constant_expression,)
        return (*production.list_of_arguments, production.constant_expression)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.3.3 Expressions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # @_(  # noqa: F821
    #     # Priority level 1
    #     # "unary_operator constant_primary",
    #     "PLUS     constant_primary %prec UPLUS",
    #     "MINUS    constant_primary %prec UMINUS",
    # )
    # # pylint: disable=no-self-use
    # def constant_expression(self, production: Production):
    #     """
    #     constant_expression ::= constant_primary
    #                           | unary_operator constant_primary
    #                           | constant_expression binary_operator constant_expression
    #                           | constant_expression "?" constant_expression ":" constant_expression
    #                           | constant_inside_expression
    #     """
    #     return ("constant_expression", production[0], production.constant_primary)

    # constant_expression ::= constant_primary
    #                         | unary_operator constant_primary
    #                         | constant_expression binary_operator constant_expression
    #                         | constant_expression "?" constant_expression ":" constant_expression
    #                         | constant_inside_expression

    @_("constant_primary")  # noqa: F821
    # pylint: disable=no-self-use
    def constant_expression(self, production: Production):
        """constant_expression ::= constant_primary"""
        primary = production[0]
        return primary.value if isinstance(primary, IntegralNumber) else primary

    @_(  # noqa: F821
        # Priority level 1
        # "unary_operator constant_primary",
        "PLUS     constant_primary %prec UPLUS",  # +
        "MINUS    constant_primary %prec UMINUS",  # -
        "LNOT     constant_primary %prec ULNOT",  # !
        "NOT      constant_primary %prec UNOT",  # ~
        "AND      constant_primary %prec UAND",  # &
        "OR       constant_primary %prec UOR",  # |
        "XOR      constant_primary %prec UXOR",  # ^
        "NAND     constant_primary %prec UNAND",  # ~&
        "NOR      constant_primary %prec UNOR",  # ~|
        "XNOR     constant_primary %prec UXNOR",  # ~^ ^~
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_expression(self, production: Production):  # noqa: F811
        """constant_expression ::= unary_operator constant_primary"""
        # print(production.constant_primary)
        # print(production[0])
        # print(production[1])

        primary: IntegralNumber = production.constant_primary

        return self.operations.uniary_op[production[0]](primary.value)

    @_(  # noqa: F821
        # Priority level 2
        # "constant_expression binary_operator constant_expression",
        "constant_expression POWER   constant_expression",
        # Priority level 3
        "constant_expression TIMES   constant_expression",
        "constant_expression DIVIDE  constant_expression",
        "constant_expression MOD     constant_expression",
        # Priority level 4
        "constant_expression PLUS    constant_expression",
        "constant_expression MINUS   constant_expression",
        # Priority level 5
        "constant_expression LSHIFT  constant_expression",
        "constant_expression RSHIFT  constant_expression",
        "constant_expression LSHIFTA constant_expression",
        "constant_expression RSHIFTA constant_expression",
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_expression(self, production: Production):  # noqa: F811
        """constant_expression := constant_expression binary_operator constant_expression"""
        return self.operations.binary_op[production[1]](
            production.constant_expression0, production.constant_expression1
        )

    @_(  # noqa: F821
        # Priority level 6
        "constant_inside_expression"
        # "constant_expression INSIDE "{" open_range_list "}""
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_expression(self, production: Production) -> bool:  # noqa: F811
        """constant_expression ::= constant_inside_expression"""
        print(">>>>>>>>>>>>>")
        return bool(production.constant_inside_expression)

    @_(  # noqa: F821
        # Priority level 6
        "constant_expression LT      constant_expression",
        "constant_expression GT      constant_expression",
        "constant_expression LE      constant_expression",
        "constant_expression GE      constant_expression",
        # Priority level 7
        "constant_expression EQ      constant_expression",
        "constant_expression NE      constant_expression",
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_expression(self, production: Production):  # noqa: F811
        """constant_expression := constant_expression binary_operator constant_expression"""
        return self.operations.comparison_op[production[1]](
            production.constant_expression0, production.constant_expression1
        )

    @_(  # noqa: F821
        # Priority level 8
        "constant_expression AND     constant_expression",
        "constant_expression XOR     constant_expression",
        "constant_expression XNOR    constant_expression",
        # Priority level 9
        "constant_expression OR      constant_expression",
        # Priority level 10
        "constant_expression LAND    constant_expression",
        # Priority level 11
        "constant_expression LOR     constant_expression",
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_expression(self, production: Production):  # noqa: F811
        """constant_expression := constant_expression binary_operator constant_expression"""
        return self.operations.bitwise_logical_op[production[1]](
            production.constant_expression0, production.constant_expression1
        )

    @_(  # noqa: F821
        # Priority level 12
        "constant_expression COND    constant_expression COLON constant_expression",
        # Priority level 13
        "constant_expression IMPL    constant_expression",
        "constant_expression EQUIV   constant_expression",
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_expression(self, production: Production):  # noqa: F811
        """constant_expression := constant_expression binary_operator constant_expression"""
        return production

    @_("constant_expression", "constant_part_select_range")  # noqa: F821
    # pylint: disable=no-self-use
    def constant_range_expression(self, production: Production):
        """constant_range_expression ::= constant_expression | constant_part_select_range"""
        return production

    @_("constant_range", "constant_indexed_range")  # noqa: F821
    # pylint: disable=no-self-use
    def constant_part_select_range(self, production: Production):
        """constant_part_select_range ::= constant_range | constant_indexed_range"""
        return production

    @_("constant_expression COLON constant_expression")  # noqa: F821
    # pylint: disable=no-self-use
    def constant_range(self, production: Production):
        """constant_range ::= constant_expression ":" constant_expression"""
        return production

    @_(  # noqa: F821
        "constant_expression PLUSCOLON  constant_expression", "constant_expression MINUSCOLON constant_expression"
    )
    # pylint: disable=no-self-use
    def constant_indexed_range(self, production: Production):
        """constant_indexed_range ::= constant_expression "+:" constant_expression
        | constant_expression "-:" constant_expression
        """
        return production

    @_(  # noqa: F821
        "constant_expression INSIDE '{' open_range_list '}'",
    )
    # pylint: disable=no-self-use
    def constant_inside_expression(self, production: Production):
        """constant_inside_expression ::= constant_expression "inside" "{" open_range_list "}" """
        print(">>>>>>>>>>>>>>>>")
        print(production.constant_expression)
        print(production.open_range_list)
        print(type(production.constant_expression in production.open_range_list))
        print(isinstance(production.constant_expression in production.open_range_list, bool))
        return bool(production.constant_expression in production.open_range_list)

    # value_range ::= constant_expression | "[" constant_expression ":" constant_expression "]"
    @_("constant_expression")  # noqa: F821
    # pylint: disable=no-self-use
    def value_range(self, production: Production):
        """value_range ::= constant_expression"""
        return production.constant_expression

    @_(" '[' constant_expression COLON constant_expression ']' ")  # noqa: F821
    # pylint: disable=no-self-use,function-redefined
    def value_range(self, production: Production):  # noqa: F811
        """value_range ::= "[" constant_expression ":" constant_expression "]" """
        # print([item for sublist in list(range(production.constant_expression0,
        #                                       production.constant_expression1 + 1)) for item in sublist])

        print(f"value: {production.constant_expression0}, type: {type(production.constant_expression0)}")
        print(f"value: {production.constant_expression1}, type: {type(production.constant_expression1)}")

        return list(range(production.constant_expression0, production.constant_expression1 + 1))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.3.4 Primaries
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # constant_primary ::= primary_literal
    #                     | parameter_identifier constant_select
    #                     | constant_concatenation [ "[" constant_range_expression "]" ]
    #                     | constant_multiple_concatenation [ "[" constant_range_expression "]" ]
    #                     | "(" constant_expression ")"
    #                     | constant_streaming_expression
    #                     | constant_cast
    #                     | math_function_call
    #                     | constant_assignment_pattern  # pylint: disable=no-self-use

    # @staticmethod
    @_("primary_literal")  # noqa: F821
    # pylint: disable=no-self-use
    def constant_primary(self, production: Production):  # pylint: disable=no-self-use
        """constant_primary ::= primary_literal"""
        return production[0]

    # @staticmethod
    @_("parameter_identifier constant_select")  # noqa: F821
    # pylint: disable=no-self-use,function-redefined
    def constant_primary(self, production: Production):  # noqa: F811
        """constant_primary ::= parameter_identifier constant_select"""
        return production

    # @staticmethod
    @_(  # noqa: F821
        # "constant_concatenation          [ "[" constant_range_expression "]" ]",
        "constant_concatenation",
        "constant_concatenation          '[' constant_range_expression ']'",
        # "constant_multiple_concatenation [ "[" constant_range_expression "]" ]",
        "constant_multiple_concatenation",
        "constant_multiple_concatenation '[' constant_range_expression ']'",
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_primary(self, production: Production):  # noqa: F811
        """constant_primary
        ::= constant_concatenation
          | constant_concatenation          "[" constant_range_expression "]"
          | constant_multiple_concatenation
          | constant_multiple_concatenation "[" constant_range_expression "]"
        """
        return production

    # @staticmethod
    @_(" '(' constant_expression ')' ")  # noqa: F821
    # pylint: disable=no-self-use,function-redefined
    def constant_primary(self, production: Production):  # noqa: F811
        """constant_primary
        ::= "(" constant_expression ")"
        """
        return production.constant_expression

    # @staticmethod
    @_(  # noqa: F821
        "constant_streaming_expression",
        "constant_cast",
        "math_function_call",
        "constant_assignment_pattern_expression",
    )
    # pylint: disable=no-self-use,function-redefined
    def constant_primary(self, production: Production):  # noqa: F811
        """constant_primary
        ::= constant_streaming_expression
          | constant_cast
          | math_function_call
          | constant_assignment_pattern_expression
        """
        return production[0]

    # @staticmethod
    @_("number", "unbased_unsized_literal", "string_literal")  # noqa: F821
    # pylint: disable=no-self-use
    def primary_literal(self, production: Production):
        """primary_literal ::= number | unbased_unsized_literal | string_literal"""
        return production[0]

    # @staticmethod
    @_("""casting_type "'" '(' constant_expression ')' """)  # noqa: F821
    # pylint: disable=no-self-use
    def constant_cast(self, production: Production):
        """constant_cast ::= casting_type "'" "'(" constant_expression ")" """
        return production

    # @staticmethod
    @_(  # noqa: F821
        "",
        "constant_bit_select '[' constant_expression ']'",
    )
    # pylint: disable=no-self-use
    def constant_bit_select(self, production: Production):
        """constant_bit_select ::= { "[" constant_expression "]" }"""
        return production

    # @staticmethod
    @_(  # noqa: F821
        "constant_bit_select",
        "constant_bit_select '[' constant_part_select_range ']'",
    )
    # pylint: disable=no-self-use
    def constant_select(self, production: Production):
        """constant_select ::= constant_bit_select [ "[" constant_part_select_range "]" ]"""
        return production

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # E.6.3.5 Operators
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # @_(  # noqa: F821
    #     "PLUS", "MINUS", "LNOT", "NOT", "AND", "NAND", "OR", "NOR", "XOR", "XNOR",
    # )
    # def unary_operator(self, production: Production):
    #     """
    #     unary_operator ::= + | - | ! | ~ | & | ~& | | | ~| | ^ | ~^ | ^~
    #     """
    #     return production

    # @_(  # noqa: F821
    #     "PLUS", "MINUS", "TIMES", "DIVIDE", "MOD", "EQ", "NE", "LAND", "LOR",
    #     "POWER",
    #     "LT", "LE", "GT", "GE",
    #     "AND", "OR", "XOR", "XNOR", "RSHIFT", "LSHIFT", "RSHIFTA", "LSHIFTA", "IMPL", "EQUIV",
    # )
    # def binary_operator(self, production: Production):
    #     """
    #     binary_operator ::= + | - | * | / | % | == | != | && | || | **
    #                       | < | <= | > | >= | & | | | ^ | ^~ | ~^ | >> | << | >>> | <<< | -> | <->
    #     """
    #     return production

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # A.9.3 Identifiers
    # E.6.4 General: Identifiers
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # @staticmethod
    @_("IDENTIFIER")  # noqa: F821
    # pylint: disable=no-self-use
    def identifier(self, production: Production):
        """
        identifier ::= IDENTIFIER
        """
        return production.IDENTIFIER

    # @staticmethod
    @_("identifier")  # noqa: F821
    # pylint: disable=no-self-use
    def parameter_identifier(self, production: Production):
        """
        parameter_identifier ::= identifier
        """
        return production.identifier

    # @staticmethod
    @_("integer_math_function_identifier", "real_math_function_identifier")  # noqa: F821
    # pylint: disable=no-self-use
    def math_function_identifier(self, production: Production):
        """
        math_function_identifier ::= integer_math_function_identifier | real_math_function_identifier
        """
        return production[0]

    # pylint: disable=invalid-name
    # @staticmethod
    @_("CLOG2")  # noqa: F821
    # pylint: disable=no-self-use
    def integer_math_function_identifier(self, production: Production):
        """
        integer_math_function_identifier ::= "$clog2"
        """
        return production[0]

    # @staticmethod
    @_(  # noqa: F821
        "ASIN",
        "ACOS",
        "ACOSH",
        "ASINH",
        "ATAN",
        "ATAN2",
        "ATANH",
        "CEIL",
        "COS",
        "COSH",
        "EXP",
        "FLOOR",
        "HYPOT",
        "LN",
        "LOG10",
        "POW",
        "SIN",
        "SINH",
        "SQRT",
        "TAN",
        "TANH",
    )
    # pylint: disable=no-self-use
    def real_math_function_identifier(self, production: Production):
        """
        real_math_function_identifier ::= "$asin"  | "$acos"  | "$acosh" | "$asinh"
                                        | "$atan"  | "$atan2" | "$atanh" | "$ceil"
                                        | "$cos"   | "$cosh"  | "$exp"   | "$floor"
                                        | "$hypot" | "$ln"    | "$log10" | "$pow"
                                        | "$sin"   | "$sinh"  | "$sqrt"  | "$tan"
                                        | "$tanh"
        """
        return production[0]

    def __init__(self):
        """Initialize the operation tables for this parser."""
        self.operations = OperationMap()

    # def error(self, production: Production):
    def error(self, token: Token):
        """Parser errors."""
        if not token:
            raise ConstantExpressionParseError("Syntax error at EOF")

        # print(dir(p))
        # print(f"Syntax error at token: "{token.type}"")
        print(f"{token.lineno:4}:{token.index:4} - '{token.type}' '{token.value}'")

        raise ConstantExpressionParseError(f"Syntax error at token: '{token.type}'")

        # Just discard the token and tell the parser it"s okay.
        # self.errok()

        # # Read ahead looking for a closing "}"
        # while True:
        #     t = next(self.tokens, None)
        #     if not t or t.type == "WHITESPACE":
        #         break
        # self.restart()
        #
        # return
        #
        # if p:
        #     # print(dir(p))
        #     # print(f"Syntax error at token: "{production.type}"")
        #     print(f"{production.lineno:4}:{production.index:4} - "{production.type}" "{production.value}"")
        #     # Just discard the token and tell the parser it"s okay.
        #     self.errok()
        # else:
        #     print("Syntax error at EOF")

    # def error(self, tok):
    #     # Read ahead looking for a terminating ";"
    #     while True:
    #         tok = next(self.tokens, None)           # Get the next token
    #         if not tok or tok.type == "SEMI":
    #             break
    #         self.errok()
    #
    #     # Return SEMI to the parser as the next lookahead token
    #     return tokenok

import re

from sly import Lexer
from sly.lex import Token


# get rid of pylint error
_ = lambda *args, **kwargs: None  # noqa: E731


class ConstantExpressionLexer(Lexer):
    """SystemVerilog Constant Expression Lexer."""

    reflags = re.VERBOSE

    reserved = ("WITH",)

    operators = (
        "LOR",
        "LAND",
        "LNOT",
        "NOT",
        "AND",
        "OR",
        "XOR",
        "NAND",
        "NOR",
        "XNOR",
        # "EQL", "NEL",
        "EQ",
        "NE",
        "LT",
        "GT",
        "LE",
        "GE",
        "INSIDE",
        "LSHIFT",
        "RSHIFT",
        "LSHIFTA",
        "RSHIFTA",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "MOD",
        "POWER",
        "COND",  # EQU"ALS,
        "PLUSCOLON",
        "MINUSCOLON",
        "COLON",
        # "AT", "COMMA", "SEMICOLON", "COLON", "DOT",
        "COMMA",
        # "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "LBRACE", "RBRACE",
        # "DELAY", "DOLLER",
        "IMPL",
        "EQUIV",
        # "TICK",
        "TICK_BRACKET",
    )

    math_function_identifiers = (
        "ACOS",
        "ACOSH",
        "ASIN",
        "ASINH",
        "ATAN",
        "ATAN2",
        "ATANH",
        "CEIL",
        "CLOG2",
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

    types = (
        "SIGNED",
        "UNSIGNED",
        "BIT",
        "BYTE",
        "SHORTINT",
        "INT",
        "LONGINT",
        "SHORTREAL",
        "REAL",
    )

    tokens = (
        operators
        + reserved
        + types
        + math_function_identifiers
        + (
            "UNBASED_UNSIZED_LITERAL",
            "OCTAL_NUMBER",
            "BINARY_NUMBER",
            "DECIMAL_NUMBER",
            "HEX_NUMBER",
            "REAL_NUMBER",
            "STRING_LITERAL",
            # "INTNUMBER_BIN", "SIGNED_INTNUMBER_BIN", "INTNUMBER_OCT", "SIGNED_INTNUMBER_OCT",
            # "INTNUMBER_HEX", "SIGNED_INTNUMBER_HEX", "INTNUMBER_DEC", "SIGNED_INTNUMBER_DEC",
            # "FLOAT_NUMBER",
            "IDENTIFIER",
        )
    )

    literals = {
        # "+", "-", "*", "/", "%", "|", "&", "~", "^", "<", ">", "=", "!", "?",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        ".",
        ",",
        ";",
        ":",
        "\\",
        "'",
        '"',
        "$",
    }

    # Tokens
    BYTE = "byte"
    SHORTINT = "shortint"
    INT = "int"
    LONGINT = "longint"
    BIT = "bit"
    SHORTREAL = "shortreal"
    REAL = "real"
    SIGNED = "signed"
    UNSIGNED = "unsigned"
    INSIDE = "inside"
    WITH = "with"

    ACOSH = r"\$acosh"
    ACOS = r"\$acos"
    ASINH = r"\$asinh"
    ASIN = r"\$asin"
    ATAN2 = r"\$atan2"
    ATAN = r"\$atan"
    ATANH = r"\$atanh"
    CEIL = r"\$ceil"
    CLOG2 = r"\$clog2"
    COS = r"\$cos"
    COSH = r"\$cosh"
    EXP = r"\$exp"
    FLOOR = r"\$floor"
    HYPOT = r"\$hypot"
    LN = r"\$ln"
    LOG10 = r"\$log10"
    POW = r"\$pow"
    SIN = r"\$sin"
    SINH = r"\$sinh"
    SQRT = r"\$sqrt"
    TAN = r"\$tan"
    TANH = r"\$tanh"

    # Operator
    LOR = r"\|\|"
    LAND = r"&&"

    # EQL = "==="
    # NEL = "!=="
    EQ = r"=="
    NE = r"!="

    NAND = r"~&"
    NOR = r"~\|"
    XNOR = r"~\^ | ^~"
    OR = r"\|"
    AND = r"&"
    XOR = r"\^"
    LNOT = r"!"
    NOT = r"~"

    LSHIFTA = r"<<<"
    RSHIFTA = r">>>"
    LSHIFT = r"<<"
    RSHIFT = r">>"

    IMPL = r"->"
    EQUIV = r"<->"

    LE = r"<="
    GE = r">="
    LT = r"<"
    GT = r">"

    PLUSCOLON = r"\+:"
    MINUSCOLON = r"-:"

    POWER = r"\*\*"
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    MOD = r"%"

    COND = r"\?"
    # EQUALS = r"="

    # AT = r"@"
    COMMA = r","
    # SEMICOLON = r";"
    COLON = r":"
    # DOT = r"\."
    #
    # LPAREN = r"\("
    # RPAREN = r"\)"
    # LBRACKET = r"\["
    # RBRACKET = r"\]"
    # LBRACE = r"\{"
    # RBRACE = r"\}"
    #
    # DELAY = r"\#"
    # DOLLER = r"\$"

    # SystemVerilog 2005 Operators
    # S05 S09 S12 S17
    # TICK = r"\""
    TICK_BRACKET = "'{"

    ###########################################################################
    # A.7.5.3 System timing check event definitions
    ###########################################################################
    _ZERO_OR_ONE = "[01]"
    _Z_OR_X = "[xXzZ]"
    # _EDGE_DESCRIPTOR = (
    #     f'(?: 01 | 10 | {_Z_OR_X} {_ZERO_OR_ONE} | {_ZERO_OR_ONE} {_Z_OR_X} )'
    # )
    # _SCALAR_CONSTANT = (
    #     f"(?: 1 ' [bB] {_ZERO_OR_ONE} | ' [bB] {_ZERO_OR_ONE} | {_ZERO_OR_ONE} )"
    #     # ((?: 1? ' [bB] ) [01])
    # )

    ###########################################################################
    # A.8.7 Numbers
    # E.6.3.6 Numbers
    ###########################################################################
    # number ::= integral_number | real_number
    # integral_number ::= decimal_number | octal_number | binary_number | hex_number
    # decimal_number ::= unsigned_number
    #                  | [ size ] decimal_base unsigned_number
    #                  | [ size ] decimal_base x_digit { '_' }
    #                  | [ size ] decimal_base z_digit { '_' }
    # binary_number ::= [ size ] binary_base binary_value
    # octal_number ::= [ size ] octal_base octal_value
    # hex_number ::= [ size ] hex_base hex_value
    # sign ::= '+' | '-'
    # size ::= non_zero_unsigned_number
    # non_zero_unsigned_number ::= non_zero_decimal_digit { '_' | decimal_digit}
    # real_number ::= fixed_point_number | unsigned_number [ '.' unsigned_number ] exp [ sign ] unsigned_number
    # fixed_point_number ::= unsigned_number '.' unsigned_number
    # exp ::= 'e' | 'E'
    # unsigned_number ::= decimal_digit { '_' | decimal_digit }
    # binary_value ::= binary_digit { '_' | binary_digit }
    # octal_value ::= octal_digit { '_' | octal_digit }
    # hex_value ::= hex_digit { '_' | hex_digit }
    # decimal_base ::= "'" [s|S] "d" | "'" [s|S] "D"
    # binary_base ::= "'" [s|S] "b" | "'" [s|S] "B"
    # octal_base ::= "'" [s|S] "o" | "'" [s|S] "O"
    # hex_base ::= "'" [s|S] "h" | "'"[s|S] "H"
    # non_zero_decimal_digit ::= [1-9]
    # decimal_digit ::= [0-9]
    # binary_digit ::= x_digit | z_digit | [01]
    # octal_digit ::= x_digit | z_digit | [0-7]
    # hex_digit ::= x_digit | z_digit | [0-9a-fA-F]
    # x_digit ::= 'x' | 'X'
    # z_digit ::= 'z' | 'Z' | '?'
    # unbased_unsized_literal ::= '0 | '1 | 'z_or_x
    ###########################################################################
    UNBASED_UNSIZED_LITERAL = f" ' ( [01] | {_Z_OR_X} ) "
    _X_DIGIT = "[xX]"
    _Z_DIGIT = "[zZ?]"

    _BINARY_DIGIT = f" ( {_X_DIGIT} | {_Z_DIGIT} | {_ZERO_OR_ONE} ) "
    # _ZERO_TO_SEVEN =  ' [0-7] '
    _OCTAL_DIGIT = f" ( {_X_DIGIT} | {_Z_DIGIT} | [0-7] ) "
    _DECIMAL_DIGIT = " [0-9] "
    _NON_ZERO_DECIMAL_DIGIT = " [1-9] "
    # _HEX_CHARS =  ' [0-9a-fA-F] '
    _HEX_DIGIT = f" ( {_X_DIGIT} | {_Z_DIGIT} | [0-9a-fA-F] ) "

    _BINARY_BASE = " ' [sS]? [bB] "
    _OCTAL_BASE = " ' [sS]? [oO] "
    _DECIMAL_BASE = " ' [sS]? [dD] "
    _HEX_BASE = " ' [sS]? [hH] "

    _BINARY_VALUE = f"   {_BINARY_DIGIT}           ( _ | {_BINARY_DIGIT}  )* "
    _OCTAL_VALUE = f"   {_OCTAL_DIGIT}            ( _ | {_OCTAL_DIGIT}   )* "
    _UNSIGNED_NUMBER = f"   {_DECIMAL_DIGIT}          ( _ | {_DECIMAL_DIGIT} )* "
    _NON_ZERO_UNSIGNED_NUMBER = f" ( {_NON_ZERO_DECIMAL_DIGIT} ( _ | {_DECIMAL_DIGIT} )* ) "
    _HEX_VALUE = f"   {_HEX_DIGIT}              ( _ | {_HEX_DIGIT}     )* "

    _SIZE = f" {_NON_ZERO_UNSIGNED_NUMBER} "

    _BINARY_NUMBER = f" {_SIZE}? {_BINARY_BASE} {_BINARY_VALUE} "
    _OCTAL_NUMBER = f" {_SIZE}? {_OCTAL_BASE}  {_OCTAL_VALUE} "
    _HEX_NUMBER = f" {_SIZE}? {_HEX_BASE}    {_HEX_VALUE} | 0[xX] {_HEX_VALUE}"
    _DECIMAL_NUMBER = f""" {_SIZE}? {_DECIMAL_BASE} {_X_DIGIT} _*
                         | {_SIZE}? {_DECIMAL_BASE} {_Z_DIGIT} _*
                         | {_SIZE}? {_DECIMAL_BASE} {_UNSIGNED_NUMBER}
                         | {_UNSIGNED_NUMBER}
                       """

    _SIGN = r" [+-] "
    _EXP = r" [eE] "

    _FIXED_POINT_NUMBER = rf" {_UNSIGNED_NUMBER} [.] {_UNSIGNED_NUMBER} "
    _REAL_NUMBER = rf""" {_UNSIGNED_NUMBER} (?: [.] {_UNSIGNED_NUMBER} )? {_EXP} {_SIGN}? {_UNSIGNED_NUMBER}
                       | {_FIXED_POINT_NUMBER}
                     """
    # INTNUMBER_BIN        = " [0-9]* '      [bB] [0-1xXzZ?]       [0-1xXzZ?_]*"
    # SIGNED_INTNUMBER_BIN = " [0-9]* ' [sS] [bB] [0-1xZzZ?]       [0-1xXzZ?_]*"
    # INTNUMBER_OCT        = " [0-9]* '      [oO] [0-7xXzZ?]       [0-7xXzZ?_]*"
    # SIGNED_INTNUMBER_OCT = " [0-9]* ' [sS] [oO] [0-7xXzZ?]       [0-7xXzZ?_]*"
    # INTNUMBER_HEX        = " [0-9]* '      [hH] [0-9a-fA-FxXzZ?] [0-9a-fA-FxXzZ?_]*"
    # SIGNED_INTNUMBER_HEX = " [0-9]* ' [sS] [hH] [0-9a-fA-FxXzZ?] [0-9a-fA-FxXzZ?_]*"
    # INTNUMBER_DEC        = "([0-9]* '      [dD] [0-9xXzZ?]       [0-9xXzZ?_]*) | ([0-9][0-9_]*)"
    # SIGNED_INTNUMBER_DEC = " [0-9]* ' [sS] [dD] [0-9xXzZ?]       [0-9xXzZ?_]*"
    #
    # FLOAT_NUMBER = "((([0-9]* [.] [0-9]+) | ([0-9]+ [.])) ([eE] [-+]? [0-9]+)?) | ([0-9]+ ([eE] [-+]? [0-9]+))"

    ###########################################################################
    # A.8.8 Strings
    # E.6.3.7 Strings
    ###########################################################################
    # string_literal ::= '"' { Any_ASCII_Characters } '"'
    # STRING_LITERAL = ' " .*? " '
    STRING_LITERAL = ' " [^"\\\n]* " '

    ###########################################################################
    # A.9.3 Identifiers
    # E.6.4 General: Identifiers
    ###########################################################################
    # IDENTIFIER = \i-[:|$]][\c-[:]]*
    # IDENTIFIER = r'\i-[:|$]][\c-[:]]*'
    # IDENTIFIER  = r'[_:A-Za-z]-[:|$]][[-._:A-Za-z0-9]-[:]]*'

    IDENTIFIER = r" [a-zA-Z_] [a-zA-Z_0-9$]* | \\\S \S* "

    # Ignored pattern
    ###########################################################################
    # A.9.4 White space
    # white_space ::= space | tab | newline | eof
    ###########################################################################
    ignore = " \t\v\f"  # WHITESPACE

    def __init__(self):
        """ """
        self.nesting_level_paren = 0
        self.nesting_level_bracket = 0
        self.nesting_level_brace = 0

    # @_(string_literal)  # noqa: F821
    # def STRING_LITERAL(self, token: Token):
    #     return token

    # @staticmethod
    @_(_REAL_NUMBER)  # noqa: F821
    def REAL_NUMBER(self, token: Token):  # pylint: disable=invalid-name,no-self-use
        """Matches real numbers."""
        return token

    # @staticmethod
    @_(_BINARY_NUMBER)  # noqa: F821
    def BINARY_NUMBER(self, token: Token):  # pylint: disable=invalid-name,no-self-use
        """Matches binray numbers."""
        return token

    # @staticmethod
    @_(_OCTAL_NUMBER)  # noqa: F821
    def OCTAL_NUMBER(self, token: Token):  # pylint: disable=invalid-name,no-self-use
        """Matches octal numbers."""
        return token

    # @staticmethod
    @_(_HEX_NUMBER)  # noqa: F821
    def HEX_NUMBER(self, token: Token):  # pylint: disable=invalid-name,no-self-use
        """Matches hexadecimal numbers."""
        return token

    # @staticmethod
    @_(_DECIMAL_NUMBER)  # noqa: F821
    def DECIMAL_NUMBER(self, token: Token):  # pylint: disable=invalid-name,no-self-use
        """Matches decimal numbers."""
        # token.value = int(token.value)
        return token

    # @_(_IDENTIFIER)
    # def IDENTIFIER(self, token: Token):
    #     """Matches identifiers.
    #     """
    #     token.type = self.reserved.get(token.value, 'IDENTIFIER')
    #     return token

    @_(r"\(")  # noqa: F821
    def lparen(self, token: Token):
        """Keep track of left parenthesis."""
        token.type = "("
        self.nesting_level_paren += 1
        return token

    @_(r"\)")  # noqa: F821
    def rparen(self, token: Token):
        """Keep track of right parenthesis."""
        token.type = ")"
        self.nesting_level_paren -= 1
        return token

    @_(r"\[")  # noqa: F821
    def lbracket(self, token: Token):
        """Keep track of left bracket."""
        token.type = "["
        self.nesting_level_bracket += 1
        return token

    @_(r"\]")  # noqa: F821
    def rbracket(self, token: Token):
        """Keep track of right bracket."""
        token.type = "]"
        self.nesting_level_bracket -= 1
        return token

    @_(r"\{")  # noqa: F821
    def lbrace(self, token: Token):
        """Keep track of left brace."""
        token.type = "{"
        self.nesting_level_brace += 1
        return token

    @_(r"\}")  # noqa: F821
    def rbrace(self, token: Token):
        """Keep track of right brace."""
        token.type = "}"
        self.nesting_level_brace -= 1
        return token

    @_(r"\r?\n+")  # noqa: F821
    def newline(self, token: Token):
        """Keep track of lines."""
        self.lineno += token.value.count("\n")

    def find_column(self, token: Token):
        """Compute token column"""
        i = token.index
        while i > 0:
            if self.text[i - 1] == "\n":
                break
            i -= 1

        column = token.index - i + 1

        return column

    # def error(self, token: Token):
    #     print(f'Illegal character: "{t.value[0]}"')
    #     self.index += 1
    #     # raise LexError(f'Illegal character: "{t.value[0]}"')

    def error(self, t: Token):
        """Lexer errors."""
        # column = find_column(self.text, t)
        column = self.find_column(t)
        lines = self.text.split("\n")

        # print(t)
        print(f"  {'-' * 80}")
        print(f'  Illegal character "{t.value[0]}" on line: {t.lineno}, column: {column}')
        print(f"  {'-' * 80}")
        if t.lineno > 2:
            print(f"  {t.lineno - 2}: {lines[t.lineno - 3]}")
        if t.lineno > 1:
            print(f"  {t.lineno - 1}: {lines[t.lineno - 2]}")
        # token_line = t.value.split('\n')[0]
        print(f"  {t.lineno}: {lines[t.lineno - 1]}")
        print(f"  {'^':>{len(str(t.lineno)) + 2 + column}}")
        if t.lineno + 1 < len(lines):
            print(f"  {t.lineno + 1}: {lines[t.lineno]}")
        if t.lineno + 2 < len(lines):
            print(f"  {t.lineno + 2}: {lines[t.lineno + 1]}")
        if t.lineno + 3 < len(lines):
            print(f"  {t.lineno + 3}: {lines[t.lineno + 2]}")
        print(f"  {'-' * 80}")
        # skip
        self.index += 1
        # raise LexError(f'Illegal character {t.value[0]!r} at index {self.index}')
        # sys.exit()

        # # Read ahead looking for a terminating ";"
        # while True:
        #     t = next(self.tokens, None)           # Get the next token
        #     if not t or t.type == 'WHITESPACE':
        #         break
        #     self.errok()
        #
        # # Return WHITESPACE to the parser as the next lookahead token
        # return tokenok

        # "ERROR: Skipping unrecognized token {production.type}, ({production.value} at
        #    line: {production.lineno}, and column: {find_column(production.lexer.lexdata, p)}

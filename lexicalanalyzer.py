import re

# Define the token types and corresponding regular expressions
KEYWORDS = ['INT', 'FLOAT', 'CHAR', 'IF', 'ELSE', 'WHILE', 'RETURN']
OPERATORS = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
SYMBOLS = [';', '(', ')', '{', '}', ',']

# Regular expressions for different token types
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),   # Integer or decimal number
    ('ID',       r'[A-Za-z_]\w*'),  # Identifiers
    ('OP',       r'==|!=|<=|>=|[+\-*/=<>{}]'),  # Operators
    ('SYMBOL',   r'[();,]'),        # Symbols (punctuation)
    ('KEYWORD',  r'\b(?:' + '|'.join(KEYWORDS) + r')\b'),  # Keywords
    ('NEWLINE',  r'\n'),            # Line endings
    ('SKIP',     r'[ \t]+'),        # Skip spaces and tabs
    ('MISMATCH', r'.'),             # Any other character
]

# Compile the token regular expressions
token_re = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
token_re = re.compile(token_re)

# Function to tokenize input code
def tokenize(code):
    tokens = []
    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in KEYWORDS:
            kind = 'KEYWORD'
        elif kind == 'NEWLINE':
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        tokens.append((kind, value))
    return tokens

# Example input code based on the provided grammar
example_code = """
INT x;
FLOAT y;
x = 10 + 2;
IF (x > y) {
    RETURN x;
} ELSE {
    RETURN y;
}
"""

# Tokenizing the example code
tokens = tokenize(example_code)

# Output the tokens
for token in tokens:
    print(token)

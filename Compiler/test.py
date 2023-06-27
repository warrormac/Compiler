import re

# Token definitions
reserved_words = {
    'print': 'print_key',
    'for': 'for_key',
    'if': 'if_key',
    'else': 'else_key',
}

operators = {
    '(': 'parentesisA',
    ')': 'parentesisC',
    '{': 'llaveA',
    '}': 'llaveC',
    '=': 'igual',
    '[': 'corcheteA',
    ']': 'corcheteC',
    ',': 'separador',
    '<': 'menor',
    '->': 'arrow_operator',
}

token_specs = [
    ('tokenInt', r'\d+'),  # Integer literals
    ('id', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identifiers
    ('operator', '|'.join(re.escape(op) for op in operators)),  # Operators
    ('reserved', '|'.join(re.escape(word) for word in reserved_words)),  # Reserved words
]

token_regex = re.compile('|'.join('(?P<%s>%s)' % spec for spec in token_specs))


def scan(code):
    tokens = []
    errors = []
    lines = code.split("\n")
    for line_number, line in enumerate(lines, start=1):
        words = line.split()
        for word in words:
            if word in reserved_words:
                tokens.append(("reserved", word))
            elif word in operators:
                tokens.append(("operator", word))
            elif word.isdigit():
                tokens.append(("int", word))
            else:
                tokens.append(("id", word))
                errors.append(("Invalid identifier", word, line_number))
    return tokens, errors


def parse(tokens):
    root = []
    current_node = root
    stack = [root]
    errors = []

    for token_type, token_value in tokens:
        if token_type == "reserved":
            if token_value in ["print", "for", "if", "else"]:
                node = ("assign", token_value, [])
                current_node.append(node)
                stack.append(current_node)
                current_node = node[2]
        elif token_type == "operator":
            if token_value == "(":
                node = ("(", [])
                current_node.append(node)
                stack.append(current_node)
                current_node = node[1]
            elif token_value == ")":
                current_node = stack.pop()
            elif token_value == "{":
                node = ("{", [])
                current_node.append(node)
                stack.append(current_node)
                current_node = node[1]
            elif token_value == "}":
                current_node = stack.pop()
            elif token_value == ",":
                continue
            elif token_value == "=":
                node = ("=", [])
                current_node.append(node)
                current_node = node[1]
            elif token_value == "[":
                node = ("[", [])
                current_node.append(node)
                stack.append(current_node)
                current_node = node[1]
            elif token_value == "]":
                current_node = stack.pop()
            elif token_value == "<":
                node = ("<", [])
                current_node.append(node)
                current_node = node[1]
            elif token_value == "->":
                node = ("->", [])
                current_node.append(node)
                current_node = node[1]
        elif token_type == "id" or token_type == "int":
            node = (token_type, token_value)
            current_node.append(node)
        else:
            errors.append(("Invalid token", token_value))

    return root, errors


def print_tree(node, level=0):
    indent = "│   " * level

    if isinstance(node, tuple):
        if node[0] == "assign":
            print(indent + "└── " + node[1])
            if isinstance(node[2], list):
                for child in node[2]:
                    print_tree(child, level + 1)
            else:
                print_tree(node[2], level + 1)
        elif node[0] == "(":
            print(indent + "├── " + node[0])
            print_tree(node[1], level + 1)
        else:
            print(indent + "└── " + node[0])
            print_tree(node[1], level + 1)
    elif isinstance(node, list):
        print(indent + "├── [")
        for child in node:
            print_tree(child, level + 1)
        print(indent + "│   " * level + "]")
    else:
        print(indent + "└── " + str(node))


file_path = 'mycode.txt'  # Replace with the path to your text file
with open(file_path, 'r') as file:
    code = file.read()

tokens, errors = scan(code)
tree, parse_errors = parse(tokens)

# Print the syntax tree
print_tree(tree)

# Print the errors
print("Errors:")
for error_type, error_value, line_number in errors + parse_errors:
    print(f"{error_type}: {error_value} (line {line_number})")

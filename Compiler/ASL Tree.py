import ast

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        result = "│   " * level + "├── " + self.name + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result





def build_tree(node, parent=None):
    node_name = node.__class__.__name__
    current_node = Node(node_name)
    if parent is not None:
        parent.add_child(current_node)
    for field_name, field_value in ast.iter_fields(node):
        if isinstance(field_value, list):
            for item in field_value:
                if isinstance(item, ast.AST):
                    build_tree(item, parent=current_node)
        elif isinstance(field_value, ast.AST):
            build_tree(field_value, parent=current_node)




def get_node_name(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Num):
        return str(node.n)
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.BinOp):
        return type(node.op).__name__
    return None

with open('mycode.txt', 'r') as file:
    code = file.read()

tree = ast.parse(code, mode='exec')
root = Node("program")
build_tree(tree, parent=root)

print(root)

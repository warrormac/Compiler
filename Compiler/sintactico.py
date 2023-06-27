from inspect import stack
from lexico import *

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import re
# class Nodo:
#     def __init__(self, ):
#         self.valor = None
#         self.hijos = []


class Gramatica:

    def __init__(self):
        self.gram = {}
        self.primeros = {}
        self.follow = {}

        self.word = None
        self.cargarGramatica()

    def nextWord(self):
        self.word = scanner.getNextToken()
        self.count += 1
        print("WORD:", self.word)

    def Fail(self, message):
        print(message)
        return False

    def main(self):
        scanner.setPos()
        # self.tree = Nodo()
        self._stack = []
        self.root = Node("G")
        self.parent = self.root
        self.grandParent = [self.root]
        self.lastStatement = None
        self.correct = True
        self.code = ""
        self.countIfStatement = 0
        self.count=0
        self.errorCount = 0

        #self.words = codigo.split()
        result = self.Program()
        print("RESULT:", result)

    # -> StatementList s
    def Program(self):
        self.nextWord()
        print("In program", self.word)
        if self.StatementList():  # program -> StatementList $
            return self.word[1] == "$"

        return self.correct

    # StatementList -> Statement StatementList
    # StatementList -> @
    def StatementList(self):
        print("In StatementList", self.word)
        self.parent = self.grandParent.pop()  # G
        if self.Statement():
            if self.word[1] != "$":
                return self.StatementList()

        if self.word[1] in self.follow["StatementList"] or (self.word[0] == "id" and self.word[0] in self.follow["StatementList"]):
            return True
        # Separar el token padre de la produccion

        return False

    # Statement -> PrintStatement
    def Statement(self):
        print("In Statement", self.word)
        if self.PrintStatement() or  \
                self.AssignmentStatement() or \
                self.ForStatement() or \
                self.IfStatement():
            return True
        # self.correct = False
        return self.Fail("Expected something else in ")

    # => id = Expr
    def AssignmentStatement(self):
        print("In Assigment", self.word)
        if self.word[0] == "id":
            self.lastStatement = "Assigment Statement"
            self.grandParent.append(self.parent)
            self._stack.append(self.word[1])  # id
            self.nextWord()
            if self.word[1] == "=":
                base = Node("=", self.parent)  # (=, G)
                self.parent = base  # =
                # self._stack.append("=")
                tokenID = self._stack.pop()  # id
                idN = Node(tokenID, self.parent)  # (id, =)

                if self.countIfStatement:
                    for i in range(self.countIfStatement):
                        self.code +="\t"
                    
                self.code += tokenID + " = "
                self.nextWord()
                if self.Expr():
                    if len(self._stack):
                        tokenStack = self._stack.pop()
                        self.code += tokenStack + "\n"
                        if self.countIfStatement:
                            for i in range(self.countIfStatement):
                                self.code +="\t"
                        tokenN = Node(tokenStack, self.parent)
                # elif self.List():
                    return True

    # => for Expr in Iterable {StatementList}
    def ForStatement(self):
        print("In For Statement", self.word)
        if self.word[1] == "for":
            self.lastStatement = "for Statement"
            forN = Node("For", self.parent)
            self.grandParent.append(self.parent)
            self.parent = forN
            self.nextWord()
            if self.Expr():  #
                xN = Node("X", forN)
                factorStack = self._stack.pop()
                factorN = Node(factorStack, xN)

                if self.word[1] == "in":
                    IterableN = Node("L", forN)
                    self.parent = IterableN
                    self.nextWord()
                    if self.Iterable():
                        BodyN = Node("Body", forN)
                        self.grandParent.append(BodyN)

                        if self.word[1] == "{":
                            self.nextWord()
                            if self.StatementList():
                                if self.word[1] == "}":
                                    self.nextWord()
                                    return True
                        else:
                            self.errorCount +=1
                            s = "*******Expected '{', but found" + self.word[1] + "token"
                            return self.Fail(s)
                else:
                    return self.Fail("Expected 'in' statement")
    # => if Expr {StatementList}
    # => if Expr {StatementList} else {StatementList}

    def IfStatement(self):
        print("In If Statement", self.word)
        if self.word[1] == "if":
            # if self.code[-1] != "\n":
            #     self.code += "\n"
            
            if self.countIfStatement:
                for _ in range(self.countIfStatement):
                    self.code += "\t"
            self.code += "if "
            self.lastStatement = "if Statement"
            self.grandParent.append(self.parent)
            ifN = Node("if", self.parent)
            self.parent = ifN
            self.nextWord()
            if self.Expr():  # condicional
                if self.word[1] == "{":
                    self.code += ":\n"
                    self.countIfStatement += 1
                    self.nextWord()
                    bodyN = Node("Then", ifN)
                    self.grandParent.append(ifN)
                    self.grandParent.append(bodyN)
                    self.parent = bodyN
                    if self.StatementList():  # body
                        if self.word[1] == "}":
                            self.countIfStatement -= 1

                            self.nextWord()
                            # Puede tener else
                            self.parent = ifN
                            return self.ElseStatement()  # else

    def ElseStatement(self):
        if self.word[1] == "else":
            if self.code[-1] != "\n":
                self.code += "\n"
                
            if self.countIfStatement:
                for _ in range(self.countIfStatement):
                    self.code += "\t"

            self.code += "else"
            elseN = Node("else", self.parent)
            # self.grandParent.append(self.parent)
            self.parent = elseN
            self.nextWord()
            if self.word[1] == "{":
                self.code += ":\n"
                self.countIfStatement += 1
                self.nextWord()
                self.grandParent.append(elseN)
                if self.StatementList():

                    if self.word[1] == "}":
                        self.countIfStatement -= 1
                        self.nextWord()
                        return True
        # Sin else
        if self.word and self.word[1] in self.follow["ElseStatement"] or (self.word[0] == "id" and self.word[0] in self.follow["ElseStatement"]):
            return True

    # => id
    # => List
    def Iterable(self):
        if self.word[0] == "id":
            self.code += self.word[1] + " "
            idN = Node(self.word[1], self.parent)  # L
            self.nextWord()
            return True
        if self.List():
            return True

    # => Expr, ExprList
    # => Expr
    #  [ 1,2,3,4,5 ]
    # def ExprList(self):
    #     if self.Expr():
    #         tokenFactor = self._stack.pop()
    #         tokenN = Node(tokenFactor, self.parent)
    #         if self.word[1] == ",":
    #             commatoseN = Node(",", self.parent)
    #             self.nextWord()
    #             if self.ExprList():
    #                 return True

    #         return True

    def PrintStatement(self):
        print("In PrintStatement", self.word)
        if self.word[1] == "print":
            self.lastStatement = "print Statement"
            self.grandParent.append(self.parent)  # G
            printN = Node("print", self.parent)

            self.parent = printN

            self.nextWord()
            if self.word[1] == "(":
                parenN = Node("(", self.parent)
                self.nextWord()
                if self.count == 3:
                    self.code += "print("
                
                if self.countIfStatement:
                    for _ in range(self.countIfStatement):
                        self.code += "\t"
                self.code += "print("
                    
                if self.Expr():
                    if self.word[1] == ")":
                        if len(self._stack):
                            lastToken = self._stack.pop()  # id int o string
                            tokenN2 = Node(lastToken, self.parent)
                            self.code += lastToken
                        
                        self.code += ")\n"
                        parenN = Node(")", printN)
                        self.nextWord()
                        return True
        return False

    # -> Expr ExprListTail
    # -> @
    def ExprList(self):
        if self.Expr():
            tokenFactor = self._stack.pop()
            tokenN = Node(tokenFactor, self.parent)
            self.code += tokenFactor + " "
            return self.ExprListTail()

        if self.word[1] in self.follow["ExprList"] or (self.word[0] == "id" and self.word[0] in self.follow["ExprList"]):
            return True

        return False

    # ExprListTail -> , Expr ExprListTail
    # ExprListTail -> @
    def ExprListTail(self):
        if self.word[1] == ",":
            self.code += ", "
            commatoseN = Node(",", self.parent)
            self.nextWord()
            if self.Expr():
                tokenFactor = self._stack.pop()
                tokenN = Node(tokenFactor, self.parent)
                self.code += tokenFactor + " "
                return self.ExprListTail()

        if self.word[1] in self.follow["ExprListTail"] or (self.word[0] == "id" and self.word[0] in self.follow["ExprListTail"]):
            return True

        return False

    # -> orExpr ExprPrime
    def Expr(self):
        # print("In Expr", self.word)
        if self.OrExpr():
            return self.ExprPrime()

    # -> and Expr ExprPrime
    # -> @
    def ExprPrime(self):
        if self.word[1] == "and":
            self.code += "and "
            self.nextWord()
            if self.Expr():
                return self.ExprPrime()

        if self.word[1] in self.follow["ExprPrime"] or (self.word[0] == "id" and self.word[0] in self.follow["ExprPrime"]):
            return True

        return False

    # -> NotExpr OrExprPrime
    def OrExpr(self):
        if self.NotExpr():
            return self.OrExprPrime()

    # -> or NotExpr OrExprPrime
    # -> @
    def OrExprPrime(self):
        if self.word[1] == "or":
            self.code += "or "
            self.nextWord()
            if self.NotExpr():
                return self.OrExprPrime()

        if self.word and self.word[1] in self.follow["OrExprPrime"] or (self.word[0] == "id" and self.word[0] in self.follow["OrExprPrime"]):
            return True

        return False

    # -> not CompExpr
    # -> CompExpr
    def NotExpr(self):
        if self.word[1] == "not":
            self.code += "not "
            self.nextWord()
            return self.CompExpr()
        return self.CompExpr()
    # ->IntExpr CompOp IntExpr
    # -> IntExpr

    def CompExpr(self):
        if self.IntExpr():
            return self.CompExprPrime()

        return False

    # compOp intExpr
    # lambda
    def CompExprPrime(self):
        if self.CompOp():
            compN = Node(self.word[1], self.parent)
            compOperator = self.word[1]
            self.parent = compN
            lastToken = self._stack.pop()
            factorN = Node(lastToken, self.parent)  # compN
            self.nextWord()
            
            self.code += lastToken + " " + compOperator
            if self.word[1] != "{":
                self.code += " "
                

            if self.IntExpr():
                if len(self._stack) and not self.IntOp():  # 1 < 1 + 1
                    lastToken = self._stack.pop()  # id int o string
                    tokenN2 = Node(lastToken, self.parent)
                    self.code += lastToken + " "
                return self.IntExprPrime()

        return self.word[1] in self.follow["CompExprPrime"] or (self.word[0] == "id" and self.word[0] in self.follow["CompExprPrime"])

    # -> Term IntExprPrime
    def IntExpr(self):
        if self.Term():
            return self.IntExprPrime()

        return False

    # -> + Term IntExprPrime
    # -> - Term IntExprPrime
    # -> @
    def IntExprPrime(self):
        if self.word[1] == "+" or self.word[1] == "-":
            plusN = Node(self.word[1], self.parent)
            self.parent = plusN

            # self._stack.append(self.word[1])  # añadir + o -
            lastToken = self._stack.pop()  # id int o string
            tokenN = Node(lastToken, self.parent)
            self.code += lastToken + " " + self.word[1] + " "
            self.nextWord()
            if (self.Term()):
                if len(self._stack) and not self.IntOp():
                    lastToken = self._stack.pop()  # id int o string
                    if self.word[1] == ")":
                        self.code += lastToken
                    else:
                        self.code += lastToken + " "
                    tokenN2 = Node(lastToken, self.parent)
                return self.IntExprPrime()

        if self.word[1] in self.follow["IntExprPrime"] or (self.word[0] == "id" and self.word[0] in self.follow["IntExprPrime"]):
            return True
        return False

    # -> Factor TermPrime
    def Term(self):
        if self.Factor():
            return self.TermPrime()

    # -> * Factor TermPrime
    # -> / Factor TermPrime
    # -> @
    def TermPrime(self):
        if self.word[1] == "*" or self.word[1] == "/":
            base = Node(self.word[1], self.parent)
            self.parent = base
            tokenPrev = self._stack.pop()
            nuevoNodo = Node(tokenPrev, self.parent)
            self.code += tokenPrev + " " + self.word[1] + " "
            self.nextWord()
            if self.Factor():
                if len(self._stack) and not self.IntOp():
                    tokenPrev = self._stack.pop()
                    nuevoNodo2 = Node(tokenPrev, self.parent)
                    if self.word[1] == ")":
                        self.code += tokenPrev
                    else:
                        self.code += tokenPrev + " "

                return self.TermPrime()

        if self.word[1] in self.follow["TermPrime"] or (self.word[0] == "id" and self.word[0] in self.follow["TermPrime"]):
            return True

        return False

    # ->( Expr)
    # ->id
    # ->tokenInt
    # ->tokenString

    def Factor(self):
        if self.word[1] == "(":
            self.code += "("
            self.nextWord()
            if self.Expr():
                if self.word[1] == ")":
                    self.code += ")"
                    self.nextWord()
                    return True

        if self.word[0] == "id" or self.word[0] == "tokenInt" \
                or self.word[0] == "tokenString":
            self._stack.append(self.word[1])
            self.nextWord()
            return True
        return False

    def List(self):
        if self.word[1] == "[":
            self.code += "["
            CorcheteN = Node(self.word[1], self.parent)
            self.nextWord()
            if self.ExprList():
                if self.word[1] == "]":
                    self.code += "]"

                    corcheteN = Node("]", self.parent)
                    self.nextWord()
                    return True

    def Boolval(self):
        return self.word[1] in ["True", "False"]

    def BoolOp(self):
        return self.word[1] in ["and", "or", "not"]

    def CompOp(self):
        return self.word[1] in ["==", "!=", "<", ">", "<=", ">="]

    def IntOp(self):
        return self.word[1] in ["+", "-", "/", "*"]

#############################################################
    def getRule(self, line):
        line = line.strip().split(":=")
        line[0] = line[0].strip()
        production = line[1].strip()
        if line[0] == "Iterable":
            print()
        if production.find("|") != -1:  # and | or
            productions = production.strip().split("|")  # [and if,    or]

            for i in range(len(productions)):
                # for production in productions:

                productions[i] = productions[i].strip().split(
                    " ")  # [[and, if ], [or]]
                for prod in productions[i]:
                    prod = prod.strip()

        else:
            productions = production.split(" ")
            for prod in productions:
                prod = prod.strip()

        return line[0], productions

    def getPrimero(self, tokenRoot, token):
        #primeros = []
        # Encontrar las apariciones del token en el lado izq de la gram
        for prod in self.gram[token]:  # [[ Statement,StatementList],[Statement]]
            if not prod[0] in self.gram.keys():  # Terminal
                self.primeros[tokenRoot].add(prod[0])
            elif prod[0] != token:  # no terminal (Recursion infinita)
                self.getPrimero(tokenRoot, prod[0])

        # return primeros

    def getFollow(self, token):
        # 1. Buscar el token en las producciones a la derecha
        for key in self.gram.keys():
            if key == "Iterable":
                print()
            for prod in self.gram[key]:
                try:
                    idx = prod.index(token)
                except:
                    idx = -1
                if idx != -1:  # token esta en la production
                    # Si existe token a su derecha

                    # verificar si idx es el ultimo indice, entonces estamos al final
                    if len(prod) == idx + 1:
                        if key in self.follow.keys():
                            for sig in self.follow[key]:
                                self.follow[token].add(sig)
                    else:
                        # primeros del token siguiente
                        if not prod[idx + 1] in self.gram.keys():  # Terminal
                            self.follow[token].add(prod[idx + 1])
                        else:  # No Terminal
                            for pri in self.primeros[prod[idx+1]]:
                                if pri != "lambda":
                                    self.follow[token].add(
                                        pri)  # si no es lambda
                                else:
                                    # print("KEy", key)
                                    # print("FOR:", token)
                                    # print("prod", self.follow[key])
                                    if key in self.follow.keys():
                                        for sig in self.follow[key]:
                                            self.follow[token].add(sig)

    def cargarGramatica(self):
        self.f = open("gramatica.txt", "r")
        for line in self.f:
            token, production = self.getRule(line)
            if token in self.gram.keys():
                self.gram[token].append(production)
            else:
                if isinstance(production[0], list):
                    self.gram[token] = []
                    for i in range(len(production)):
                        self.gram[token].append(production[i])
                else:
                    self.gram[token] = [production]

        for token in self.gram.keys():
            # set quita los dupilcados de la lista
            self.primeros[token] = set()
            self.getPrimero(token, token)
            #self.primeros[token] = set(self.primeros[token])

        for token in self.gram.keys():
            self.follow[token] = set()
            self.getFollow(token)


scanner = Scanner("mycode.txt")
# print("INFO SCAN - Start scanning… ")
scanner.read_file()

# print("INFO SCAN - COMPLETED… ")

gram = Gramatica()

for g in gram.gram:
    print(g, ':', gram.gram[g])

# print("FOLLOW")
# for token in gram.follow.keys():
#     print(token, "->", gram.follow[token])

# print("PRIMEROS")

# print("")
# for token in gram.primeros.keys():
#     print(token, "->", gram.primeros[token])

# print("")
# print("")

gram.main()
print("gram.code")
print(gram.code)

print("gram._stack")
print(gram._stack)
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
    return tokens

def parse(tokens):
    root = []
    current_node = root
    stack = [root]
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
    return root

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

tokens = scan(code)
tree = parse(tokens)
print_tree(tree)

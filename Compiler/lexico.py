# from string import punctuation as operators
# ERRORS HANDLED AT TOKENS
operators = "+-*/=><)(!{}[],"

_operators = {
    "+": "suma",
    "-": "resta",
    "*": "mult",
    "/": "division",
    "=": "igual",
    ">": "mayor",
    "<": "menor",
    ")": "parentesisC",
    "(": "parentesisA",
    "!": "negacion",
    "{": "llaveA",
    "}": "llaveC",
    "[": "corcheteA",
    "]": "corcheteC",
    ",": "separador"
}

opAllowed = ["(", ")", "[", "]", "="]

_operators2 = {
    "==": "Comparacion",
    "!=": "diferente",
    "<=": "menorI",
    ">=": "mayorI",
    "->": "arrow_operator"
}

# operators2 = "><="
reserved = {
    "if": "if_key",
    "else": "else_key",
    "for": "for_key",
    "print": "print_key",
    "and": "and_key",
    "or": "or_key",
    "not": "not_key",
    "True": "True_key",
    "False": "False_key",
    "int": "int_key",
    "string": "string_key",
    "bool": "bool_key",
    "while": "while_key"
}

accepted_special = ['_']
n_accepted_special = ['@']
# my_language = "var1 = 1 + 2"
# my_read_position = 0


# operators = [[,]""]

class Scanner:
    def __init__(self, filename):
        # self.line = line
        self.f = open(filename, "r")
        # self.my_read_position = 0
        self.line_count = 1
        self.tokens = []

    def setPos(self):
        self.pos = 0

    def getNextToken(self):
        self.pos += 1
        if self.pos-1 != len(self.tokens):
            if self.tokens[self.pos-1][0] == "ignored":
                return self.getNextToken()
            return self.tokens[self.pos-1]
        return ["", "$"]

    def remove_spaces(self):
        while self.git_char() in " \t":
            self.get_char()

    def git_char(self):  # d
        # temp = self.line[0]se
        # self.my_read_position = self.my_read_position + 1
        return self.line[0]

    def get_char(self):  # abc

        # print("In git_char:",self.line)
        temp = self.line[0]  # a
        self.line = self.line[1:]  # bc
        return temp

    def readDigit(self):  #
        digito = self.git_char()  # el self no se pasa
        invalidToken = False
        lectura = ""
        while (digito.isdigit() or (invalidToken and digito.isalpha())):
            self.get_char()
            lectura += digito
            if self.line == "":  # last digit
                break
            digito = self.git_char()  # git char elimina alpha en token invalido: "1a1"

            # Verificar validez del token:
            if digito.isalpha():
                invalidToken = True

        if invalidToken == True:
            print('ERROR LINEA', self.line_count, "tokenInt invalid")
            print("DEBUG SCAN INT - [ invalidINT, ",
                  lectura, "]found at line: ", self.line_count)
            return ["invalid Int", lectura]

        # INT TOO LONG
        try:
            number = int(lectura)
            if number < 2147483647:
                print(
                    "DEBUG SCAN INT - [ tokenInt, ", lectura, "]found at line: ", self.line_count)
                return ["tokenInt", lectura]
            else:
                print("DEBUG SCAN INT - [ invalid Int, ",
                      lectura, "]found at line: ", self.line_count)
                return ["invalid Int", lectura]
        except Exception as e:
            print("Exception in readDigit:", e)
            print("DEBUG SCAN INT - [ invalidINT, ",
                  lectura, "]found at line: ", self.line_count)
            return ["invalid Int", lectura]

    def readAlpha(self):
        digito = self.git_char()
        badId = False
        lectura = ""
        while (digito.isalpha() or digito.isdigit() or digito == "_" or digito in n_accepted_special):
            self.get_char()

            if digito in n_accepted_special:
                badId = True

            lectura += digito
            if self.line == "":  # last digit
                break
            digito = self.git_char()

            # Palabras reservadas

        if lectura in reserved:
            print("DEBUG SCAN - RESERVED [", reserved[lectura],
                  ",", lectura, "]found at line: ", self.line_count)
            return [reserved[lectura], lectura]
        elif badId:
            print("DEBUG SCAN - [ InvalidId, ", lectura,
                  "]found at line: ", self.line_count)
            return ["InvalidId", lectura]

        print("DEBUG SCAN - [ ID, ", lectura,
              "]found at line: ", self.line_count)
        return ["id", lectura]

    def readString(self):
        comilla = self.git_char()
        finishComilla = comilla
        # count = 1
        self.get_char()  # Elimina Primera comilla
        digito = self.git_char()  # Lee primer caracter del string
        lectura = ""

        bs = False

        #  BLOQUE DE COMENTARIO
        if digito == comilla:
            self.get_char()
            comentario = self.git_char()
            # if digito == '"' and comentario == '"':
            if digito == comentario:
                lectura = 'ignored'
                self.line = self.line[-1]
                print("DEBUG SCAN - COMENTARIO [",
                      "comentario, '", lectura, "']")
                return [lectura, "comentario"]

        # if comilla == "'":
        while (digito != finishComilla or bs):
            if bs:
                bs = False
            self.get_char()
            lectura += digito

            if digito == '\\':
                bs = True

            if self.line == "" or self.line == '\n':  # last digit
                print('ERROR LINEA', self.line_count, "invalid str")
                print("DEBUG SCAN - STRING [", "invalid str, '",
                      lectura, "'] found at line: ", self.line_count)
                return ["invalid str", lectura]
            digito = self.git_char()

        # if comilla == '"':
        #     while ( digito != '"'):
        #         self.get_char()
        #         lectura += digito
        #         if self.line == "" or self.line == '\n':  # last digit
        #             print('ERROR LINEA', self.line_count, "invalid str")
        #             return ["invalid str", lectura]

        #         digito = self.git_char()

        self.get_char()  # Elimina ultima comilla
        print("DEBUG SCAN - STRING [", "tokenString, '",
              lectura, "'] found at line: ", self.line_count)
        return ["tokenString", lectura]

    def readOperator(self):  # >= $55s5
        count = 0
        digito = self.git_char()
        lectura = ""  # in operators

        badOpE = -1
        badOpI = -1
        while (digito in operators):
            count += 1
            self.get_char()  # >
            lectura += digito  # >
            if self.line == "":  # last digit
                break
            digito = self.git_char()  # =

        # if badOp:
        #     return ["Invalid operator", lectura]

        if count > 2:  # ((1 *2)(mod 2))>= pepito
            # )>=
            operator_list = []
            op = ""
            i = 0
            while i < count:
                op = lectura[i]
                if i == badOpI and badOpE != -1:
                    op = lectura[i:badOpE]  # )+++-
                    operator_list.append(["invalid operator", op])
                    i = badOpE - 1

                # +=
                elif i + 1 != count and op + lectura[i + 1] in _operators2.keys():
                    op = op + lectura[i + 1]
                    operator_list.append([_operators2[op], op])
                    i = i + 1  # Saltar el segundo operador
                else:  # len(op) = 1 # ()
                    operator_list.append([_operators[op], op])  # op=(

                i = i + 1

            return ["operator", operator_list]
            # count = 0
            # print('ERROR LINEA', self.line_count, "invalid operator")
            # return ["invalid operator", lectura]

        if count == 2:
            if lectura[0] == lectura[1] and not lectura[0] in opAllowed:
                print("DEBUG SCAN - OPERATOR[", "invalid operator,",
                      lectura, "]found at line: ", self.line_count)
                return ["invalid operator", lectura]

            if lectura in _operators2.keys():
                print("DEBUG SCAN - OPERATOR[", _operators2[lectura],
                      ",", lectura, "]found at line: ", self.line_count)
                return [_operators2[lectura], lectura]
            else:

                #     # print('ERROR LINEA', self.line_count, "invalid operator")
                print("DEBUG SCAN - OPERATOR",
                      _operators[lectura[0]], lectura[0], "found at line: ", self.line_count)
                print("DEBUG SCAN - OPERATOR",
                      _operators[lectura[1]], lectura[1], "found at line: ", self.line_count)
                return ["operator", [[_operators[lectura[0]], lectura[0]],
                                     [_operators[lectura[1]], lectura[1]]
                                     ]
                        ]

        count = 0
        print("DEBUG SCAN - OPERATOR [", _operators[lectura],
              ",", lectura, "]found at line: ", self.line_count)
        return [_operators[lectura], lectura]  # [suma, '+']

    def read_file(self):
        for line in self.f:
            self.line = line
            self.read_line()
            self.line_count += 1
        self.f.close()
        # return self.tokens

    def read_line(self):
        while self.line != "":  # last digit
            c = self.git_char()
            if c == '\n':
                break
            # Comment
            if c == '#':
                # self.get_char()
                # if self.line[-1] == '\n':
                #     lectura = self.line[:-1]
                # else:
                #     lectura = self.line

                lectura = 'ignored'
                self.line = self.line[-1]
                print("DEBUG SCAN - COMENTARIO [",
                      "comentario, '", lectura, "']")
                self.tokens.append([lectura, "comentario"])
                break
            # Number .isdigit()
            elif c.isdigit():
                self.tokens.append(self.readDigit())  # " + 2"

            # Variable .isalpha()
            elif c.isalpha() or c == "_":
                self.tokens.append(self.readAlpha())
            # String literal
            elif c == '"' or c == "'":
                self.tokens.append(self.readString())
            # Operator
            elif c in operators:
                response = self.readOperator()
                if type(response[1]) is list:
                    for op in response[1]:
                        # print("DEBUG SCAN - OPERATOR", op, "found at line: ", self.line_count)
                        self.tokens.append(op)
                else:
                    self.tokens.append(response)

            # Space
            elif c in " \t\n":
                self.remove_spaces()
            else:
                lectura = self.git_char()
                return ["invalid token", lectura]
                break


# f = open("mycode.txt", "r")
# print("Lines read")
# for line in f:
#     print(line)
# f.close()

# scanner = Scanner("mycode.txt")
# print("INFO SCAN - Start scanning… ")
# scanner.read_file()
# print("INFO SCAN - COMPLETED… ")
# # print(*tokens, sep='\n')
# # # ERRORS HANDLED IN TOKENS

#Leer archivo
def write_code():
    return (open('codigo.txt', 'r')).read()

#leemos el archivo codigo a la varible codigo
codigo = write_code()

#Creamos variales para saber la posicion, fila e iterador
iter = 0        #Donde esta apuntando en el codigo
iter_f = 1      #Numero de Fila
iter_c = 0      #Numero de columna
tokens = []     #Tokens
tokens_e = []
#Funciones para identificar los tokens y palabras claves

#Para identificar operadores
def IntOp(char):
    intop = ['+', '*', '/']
    if char == '-':
        # Check if it is a subtraction or an arrow
        if codigo[iter:iter+2] == '->':
            return False
        else:
            return True
    elif char in intop:
        return True
    else:
        return False

#Para identificar asignacion
def AsigOp(char):
    asigop = ['=']
    if(char in asigop):
        return True
    return False

#Para identificar operadores de comparacion
def CompOp(string):
    comop = ['!','==', '!=', '<', '>', '<=', ">=","//","%",",",":","."]
    if codigo[iter:iter+2] == "->":
        return True
    elif string in comop:
        return True
    else:
        return False

#Para identificar asignacion
def AsigOp(char):
    asigop = ['=']
    if(char in asigop):
        return True
    return False

#Para identificar operadores de comparacion
def CompOp(string):
    comop = ['!','==', '!=', '<', '>', '<=', ">=","//","%",",",":","."]
    if codigo[iter:iter+2] == "->":
        return True
    elif string in comop:
        return True
    else:
        return False
#Para identificar palabras claves
def WordKeys(string):
    wordkeys = ['for', 'if', 'else', 'in', 'list','range','as', 'assert','async','await','break','class','continue','def','del','elif','except','finally','from','global','import','is','lambda','nonlocal','pass','raise','return','try','while','with','yild']
    if(string in wordkeys):
        return True
    return False

#Para identificar valor de Bool
def BoolVal(string):
    boolop = ['false', 'true']
    if(string in boolop):
        return True
    return False

#Para identificar operadores booleanos 
def BoolOp(string):
    boolop = ['and', 'or', 'not']
    if(string in boolop):
        return True
    return False

def Delimiter(letter):
    
    delimiter = ['(',')','{','}','[',']']
    token = ""
    if letter in delimiter:
        if letter == '(':
            tokens = (Token("OpenPar", PeekChar(), iter_f, iter_c))
        elif letter == ')':
            tokens = (Token("ClosePar", PeekChar(), iter_f, iter_c))
        elif letter == '{':
            tokens = (Token("OpenKey", PeekChar(), iter_f, iter_c))
        elif letter == '}':
            tokens = (Token("Closekey", PeekChar(), iter_f, iter_c))
        elif letter == '[':
            tokens = (Token("OpenList", PeekChar(), iter_f, iter_c))
        elif letter == ']':
            tokens = (Token("CloseList", PeekChar(), iter_f, iter_c))
        return [True,tokens]
    return [False]

def Id():
    global iter
    global iter_c
    id = "abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    string_id = ""
    while codigo[iter] in id:
        string_id += codigo[iter]
        iter += 1
        iter_c += 1
    return string_id


def Number():
    global iter
    global iter_c
    number = "0123456789"
    string_number = ""

    if codigo[iter] == '0' and codigo[iter + 1] in number:
        while codigo[iter] == '0':
            iter += 1
            iter_c += 1

        while codigo[iter] in number:
            string_number += codigo[iter]
            iter += 1
            iter_c += 1
    else:
        while codigo[iter] in number:
            string_number += codigo[iter]
            iter += 1
            iter_c += 1
    
    return string_number
    
def Literal(letter):
    literal = ["'",'"']
    if letter in literal:
        return True
    return False

def LeerLiteral():
    global iter
    global iter_f
    global iter_c

    l = PeekChar()
    literal = ""

    literal += codigo[iter]
    iter+=1
    bandera = True
    while codigo[iter] != l:
        if codigo[iter] == '\n':
            iter_f+=1
            iter_c=0
        iter_c+=1
        literal += codigo[iter]
        iter+=1
        if codigo[iter] == '$':
            bandera = False
            break
    literal += codigo[iter]
    
    if bandera:
        iter+=1
    else:
        iter-=1
    return literal
    
#Clase Token
class Token:
    def __init__(self, type, value, line, space):
        self.type = type
        self.value = value
        self.line = line
        self.space = space

    def ShowToken(self):
        print("{} [ {} ] found at ({}:{})".format(
            self.type, self.value, self.line, self.space))



#PeekChar
def PeekChar():
    execep = [' ', '\n', '#', "'", '"']

    global iter
    global iter_f
    global iter_c

    while (codigo[iter] in execep):
        #Posible Literal
        if codigo[iter] == '"':
            if codigo[iter:iter+3] != '"""':
                return codigo[iter]
        #Posible Literal
        if codigo[iter] == "'":
            if codigo[iter:iter+3] != "'''":
                return codigo[iter]
        #Comentario comillas dobles
        if codigo[iter:iter+3] == '"""':
            iter += 3
            iter_c += 3
            while codigo[iter] != '"':
                if codigo[iter] == '\n':
                    iter_f += 1
                    iter_c = 0
                else:
                    iter_c += 1    
                iter += 1
            if codigo[iter:iter+3] == '"""':
                iter += 3
                iter_c += 3
            iter_f+=1
        #Comentario comillas simples
        elif codigo[iter:iter+3] == "'''":
            iter += 3
            iter_c += 3
            while codigo[iter] != "'":
                if codigo[iter] == '\n':
                    iter_f += 1
                    iter_c = 0
                else:
                    iter_c += 1    
                iter += 1
            if codigo[iter:iter+3] == "'''":
                iter += 3
                iter_c += 3
            iter_f+=1
        #Saltar espacios
        elif codigo[iter] == ' ':
            iter_c += 1
        #Saltar saltos de linea
        elif codigo[iter] == '\n':
            iter_c = 0
            iter_f += 1
        #Saltar Comentario Lineal
        elif codigo[iter] == '#':
            while codigo[iter] != '\n':
                iter += 1
            iter_f += 1
            iter_c = 0
        
        iter += 1
    return codigo[iter]

#GetChar
def GetChar():
    global iter
    global iter_c
    letter = PeekChar()
    iter += 1
    iter_c += 1
    return letter

def GetToken():

    global iter
    global iter_c
    global iter_f
    global tokens
    global codigo

    letter = PeekChar()
    if letter == '$':
        codigo = ""
        return [2]
    elif Delimiter(letter)[0]:
        tokens = Delimiter(letter)[1]
        GetChar()
    elif IntOp(letter):
        tokens = (Token("IntOp", GetChar(), iter_f, iter_c))
    elif AsigOp(letter):
        if CompOp(letter + codigo[iter+1]):
            tokens = (Token("CompOp", (GetChar() + GetChar()), iter_f, iter_c))
        else:
            tokens = (Token("AsigOp", GetChar(), iter_f, iter_c))
    elif CompOp(letter):
        if CompOp(letter + codigo[iter+1]):
            tokens = (Token("CompOp", (GetChar() + GetChar()), iter_f, iter_c))
        else:
            tokens = (Token("CompOp", GetChar(), iter_f, iter_c))
    elif Literal(letter):
        tokens = (Token("Literal", LeerLiteral(), iter_f, iter_c))
    elif letter.isalpha():
        token = Id()
        if WordKeys(token):
            tokens = (Token("Wordkeys", token, iter_f, iter_c))
        elif BoolOp(token):
            tokens = (Token("BoolOp", token, iter_f, iter_c))
        elif BoolVal(token):
            tokens = (Token("BoolVal", token, iter_f, iter_c))
        else:
            tokens = (Token("Id", token, iter_f, iter_c))
    elif letter.isdigit():
        token = Number()
        tokens = (Token("Number", token, iter_f, iter_c))
    else:
        tokens = (Token("Error", GetChar(), iter_f, iter_c))
        return [0,tokens]
    return [1,tokens]

def Scanner():
    global iter
    global codigo

    error = 0
    tokens = []
    log_error = []

    if ('$' in codigo) == False:
        log_error.append(Token("Error","Sin EOF($)",codigo.count('\n'),1))
        error +=1
        codigo = codigo + '\n' + '$'


    print("INFO SCAN - Start scanning ....")
    while codigo:
        token = GetToken()
        if token[0] == 1:
            tokens.append(token[1])
            print("DEBUG SCAN - ",end="")
            token[1].ShowToken()
        elif token[0] == 0:
            error +=1
            log_error.append(token[1])
        
    print("INFO SCAN - Completed with {} errors".format(error))
    print()
    print()
    print()
    print("INFO ERRORS - {} errors".format(error))
    for i in log_error:
        print("DEBUG ERRORS - ",end="")
        i.ShowToken()
    
Scanner()

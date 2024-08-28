import ply.lex as lex
from flask import Flask, render_template, request

app = Flask(__name__)

# Definición de palabras reservadas (sin incluir 'main')
reserved = {
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'n': 'N'
}

tokens = ['PABIERTO', 'PCERRADO', 'LLAVE_ABIERTA', 'LLAVE_CERRADA', 'OPERADOR', 'SIMBOLO', 'ID'] + list(reserved.values())

# Expresiones regulares para las palabras reservadas y otros tokens
t_PUBLIC = r'public'
t_STATIC = r'static'
t_VOID = r'void'
t_N = r'n'
t_OPERADOR = r'='

# Identificadores 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verificar si es una palabra reservada
    return t

# Expresión regular para símbolos 
def t_SIMBOLO(t):
    r'[0-9]+|[.;]'
    return t

# Símbolos
t_PABIERTO = r'\('
t_PCERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios en blanco, tabulaciones y nuevas líneas
t_ignore = ' \t\r'

# Manejo de errores
def t_error(t):
    print('Caracter no válido:', t.value[0])
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        expresion = request.form.get('Expresion')
        lexer.lineno = 1  # Reiniciar el número de línea antes de procesar
        lexer.input(expresion)
        
        # Proceso de tokens en el orden en que aparecen, con número de línea
        result_lexema = []
        contador = {}  # Inicializar el diccionario de conteo
        for token in lexer:
            if token.type in reserved.values():
                result_lexema.append(("RESERVADO", token.value, token.lineno))
            elif token.type == "ID":
                result_lexema.append(("IDENTIFICADOR", token.value, token.lineno))
            elif token.type == "PABIERTO":
                result_lexema.append(("PARENTESIS IZQUIERDO", token.value, token.lineno))
            elif token.type == "PCERRADO":
                result_lexema.append(("PARENTESIS DERECHO", token.value, token.lineno))
            elif token.type == "LLAVE_ABIERTA":
                result_lexema.append(("DELIMITADOR", token.value, token.lineno))
            elif token.type == "LLAVE_CERRADA":
                result_lexema.append(("DELIMITADOR", token.value, token.lineno))
            elif token.type == "OPERADOR":
                result_lexema.append(("OPERADOR", token.value, token.lineno))
            elif token.type == "SIMBOLO":
                result_lexema.append(("SIMBOLO", token.value, token.lineno))
        
        # Contar las ocurrencias de cada tipo de token
        for tipo, palabra, numero in result_lexema:
            if tipo in contador:
                contador[tipo] += 1
            else:
                contador[tipo] = 1
        
        return render_template('index.html', tokens=result_lexema, contador=contador, expresion=expresion)
    
    return render_template('index.html', expresion=None)

if __name__ == '__main__':
    app.run(debug=True)
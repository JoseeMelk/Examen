import ply.lex as lex

class AnalizadorLexico:
    def __init__(self):
        #TOKENS
        self.tokens = ['IDENTIFICADOR', 'PALABRA_R', 'SIMBOLO', 'OPERADOR', 'NUMERO']
        
        #Expresiones regulares
        self.reserved = {
            'static': 'PALABRA_R',
            'void': 'PALABRA_R',
            'int': 'PALABRA_R',
            'float': 'PALABRA_R',
            'public': 'PALABRA_R'
        }
        self.t_SIMBOLO = r'[\(\)\{\};,]'
        self.t_OPERADOR = r'[\*\/\+\-=]'
        
        #Variables para guardar
        self.states_list = []
        self.error_undefined = 'Error indefinido, por el momento contacte con Melk'
        self.error_undefined_flag = False
        self.current_line = 1
        self.error_toke = ''
        self.error_toke_flag = False
        
        #instancia del analizador lexico de ply
        self.lexer = lex.lex(module=self)
        
    def t_IDENTIFICADOR(self, t):
        r'\b(main|([a-zA-Z]|_)\w*)\b'
        t.type = self.reserved.get(t.value, 'IDENTIFICADOR')
        return t

    def t_NUMERO(self, t):
        r'\b\d+\b'
        t.value = int(t.value)
        return t
    
    t_ignore = ' \t'
    
    def t_error(self, t):
        if t.value != '\n':
            self.error_toke = t.value
        else:
            self.current_line += 1
        self.error_toke_flag = True
        t.lexer.skip(1)
        
    def _state_list(self, token, lexema, linea):
        self.states_list.append({"token": token, "lexema": lexema, "linea": linea})
    
    def analyzer(self, data):
        self.states_list = []
        self.error_undefined_flag = False
        self.lexer.input(data)
        if self.error_toke_flag != False:
            self._state_list("Caracter ilegal", self.error_toke, self.current_line)
        while True:
            token = self.lexer.token()
            if not token:
                break
            self._state_list(token.type, token.value, self.current_line)
    
    def delete(self):
        self.states_list = []
        self.error_undefined_flag = False
        self.lexer.lineno = 1  # Reiniciar contador de línea
        self.current_line = 1
        
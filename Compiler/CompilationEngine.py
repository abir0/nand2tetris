import sys
from Tokenizer import Tokenizer
from SymbolTable import SymbolTable

class CompilationEngine:

    BINARY_OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    UNARY_OP = ["-", "~"]

    KEYWORD_CONST = ["true", "false", "null", "this"]

    SET = set(Tokenizer.KEYWORDS + Tokenizer.SYMBOLS) - set(["("] + UNARY_OP + BINARY_OP + KEYWORD_CONST)

    ENTITY = {"~": "&sim;", "&": "&amp;", "<": "&lt;", ">": "&gt;", "=": "&equals;"}

    ARITHMATIC = {"+" : "add", "-" : "sub", "*" : "Math.mult()", "/" : "Math.divide()",
                  "&" : "and", "|" : "or", "<" : "lt", ">" : "gt",
                  "=" : "eq", "-" : "neg", "~" : "not"}


    def __init__(self, tokens, vm_writer, verbose=False):
        self.Tokens = tokens
        self.vm_writer = vm_writer
        self.verbose = verbose

    def compileClass(self, symbol_table):
        self.Tokens.advance()
        if self.Tokens.keyWord() == "CLASS":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                class_name = self.Tokens.getToken()
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                #self.Tokens.identifier()
                self.Tokens.advance()
                if self.Tokens.symbol() == "{":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    while self.Tokens.keyWord() in ["STATIC", "FIELD"]:
                        self.compileClassVarDec(symbol_table=symbol_table)
                    while self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
                        symbol_table.startSubroutine()
                        if self.Tokens.keyWord() in ["CONSTRUCTOR", "METHOD"]:
                            symbol_table.define(name='this', kind='argument', type=class_name)
                        self.compileSubroutineDec(symbol_table=symbol_table)
                    if self.Tokens.symbol() == "}":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")

    def compileClassVarDec(self, symbol_table):
        if self.Tokens.keyWord() in ["STATIC", "FIELD"]:
            var_kind = self.Tokens.getToken()
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                var_type = self.Tokens.getToken()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                    self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                elif self.Tokens.tokenType() == "IDENTIFIER":
                    self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                var_name = self.Tokens.getToken()
                symbol_table.define(name=var_name, type=var_type, kind=var_kind, kind_flag=True)
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                while self.Tokens.symbol() == ",":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        var_name = self.Tokens.getToken()
                        symbol_table.define(name=var_name, type=var_type, kind=var_kind, kind_flag=True)
                        self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                        self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()

    def compileSubroutineDec(self, symbol_table):
        if self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["VOID", "INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                if self.Tokens.keyWord() in ["VOID", "INT", "CHAR", "BOOLEAN"]:
                    self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                elif self.Tokens.tokenType() == "IDENTIFIER":
                    self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                if self.Tokens.symbol() == "(":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    self.compileParameterList(symbol_table=symbol_table)
                    if self.Tokens.symbol() == ")":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.compileSubroutineBody(symbol_table=symbol_table)

    def compileParameterList(self, symbol_table):
        if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
            var_kind = 'argument'   # variable kind
            var_type = self.Tokens.getToken()   # variable type
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            elif self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
        if self.Tokens.tokenType() == "IDENTIFIER":
            var_name = self.Tokens.getToken()   # variable name
            symbol_table.define(name=var_name, type=var_type, kind=var_kind)    # define variable
            self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
            while self.Tokens.symbol() == ",":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                    var_type = self.Tokens.getToken()
                    if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                        self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                    elif self.Tokens.tokenType() == "IDENTIFIER":
                        self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                if self.Tokens.tokenType() == "IDENTIFIER":
                    var_name = self.Tokens.getToken()
                    symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                    self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                    self.Tokens.advance()

    def compileSubroutineBody(self, symbol_table):
        if self.Tokens.symbol() == "{":
            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
            self.Tokens.advance()
            while self.Tokens.keyWord() == "VAR":
                self.compileVarDec(symbol_table)
            if self.Tokens.keyWord() in ["LET", "DO", "IF", "WHILE", "RETURN"]:
                self.compileStatements()
            if self.Tokens.symbol() == "}":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()

    def compileVarDec(self, symbol_table):
        var_kind = 'local'
        if self.Tokens.keyWord() == "VAR":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                var_type = self.Tokens.getToken()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                    self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                elif self.Tokens.tokenType() == "IDENTIFIER":
                    self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                var_name = self.Tokens.getToken()
                symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                while self.Tokens.symbol() == ",":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        var_name = self.Tokens.getToken()
                        symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                        self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                        self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()

    def compileStatements(self):
        while self.Tokens.keyWord() in ["LET", "DO", "IF", "WHILE", "RETURN"]:
            if self.Tokens.keyWord() == "LET":
                self.compileLet()
            elif self.Tokens.keyWord() == "DO":
                self.compileDo()
            elif self.Tokens.keyWord() == "IF":
                self.compileIf()
            elif self.Tokens.keyWord() == "WHILE":
                self.compileWhile()
            elif self.Tokens.keyWord() == "RETURN":
                self.compileReturn()

    def compileLet(self):
        if self.Tokens.keyWord() == "LET":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                if self.Tokens.symbol() == "[":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.symbol() != "]":
                        self.compileExpression()
                        if self.Tokens.symbol() == "]":
                            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                            self.Tokens.advance()
                if self.Tokens.symbol() == "=":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.symbol() != ";":
                        self.compileExpression()
                        if self.Tokens.symbol() == ";":
                            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                            self.Tokens.advance()

    def compileDo(self):
        if self.Tokens.keyWord() == "DO":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                if self.Tokens.symbol() == "(":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    self.compileExpressionList()
                    if self.Tokens.symbol() == ")":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                elif self.Tokens.symbol() == ".":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "(":
                            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                            self.Tokens.advance()
                            self.compileExpressionList()
                            if self.Tokens.symbol() == ")":
                                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                                self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()

    def compileIf(self):
        if self.Tokens.keyWord() == "IF":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.symbol() == "(":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if self.Tokens.symbol() != ")":
                    self.compileExpression()
                    if self.Tokens.symbol() == ")":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                            self.Tokens.advance()
                            if self.Tokens.symbol() != "}":
                                self.compileStatements()
                                if self.Tokens.symbol() == "}":
                                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                                    self.Tokens.advance()
                                if self.Tokens.keyWord() == "ELSE":
                                    self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                                    self.Tokens.advance()
                                    if self.Tokens.symbol() == "{":
                                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                                        self.Tokens.advance()
                                        if self.Tokens.symbol() != "}":
                                            self.compileStatements()
                                            if self.Tokens.symbol() == "}":
                                                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                                                self.Tokens.advance()

    def compileWhile(self):
        if self.Tokens.keyWord() == "WHILE":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.symbol() == "(":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if self.Tokens.symbol() != ")":
                    self.compileExpression()
                    if self.Tokens.symbol() == ")":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                            self.Tokens.advance()
                            if self.Tokens.symbol() != "}":
                                self.compileStatements()
                                if self.Tokens.symbol() == "}":
                                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                                    self.Tokens.advance()

    def compileReturn(self):
        if self.Tokens.keyWord() == "RETURN":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.symbol() != ";":
                self.compileExpression()
            if self.Tokens.symbol() == ";":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()

    def compileExpression(self):
        if self.Tokens.getToken() not in CompilationEngine.SET:
            self.compileTerm()
            while self.Tokens.getToken() not in CompilationEngine.SET:
                if self.Tokens.symbol() in CompilationEngine.BINARY_OP:
                    command = self.ARITHMATIC[self.Tokens.getToken()]
                    self.Tokens.advance()
                    if self.Tokens.getToken() not in CompilationEngine.SET:
                        self.compileTerm()
                        self.vm_writer.writeArithmatic(command)


    def compileTerm(self):
        if self.Tokens.getToken() not in CompilationEngine.SET:
            if self.Tokens.tokenType() == "INT_CONST":
                self.vm_writer.writePush("constant", self.Tokens.getToken())
                self.Tokens.advance()
            elif self.Tokens.tokenType() == "STR_CONST":
                self.write("<stringConstant> " + self.Tokens.getToken()[1:-1] + " </stringConstant>\n")
                self.Tokens.advance()
            elif self.Tokens.getToken() in CompilationEngine.KEYWORD_CONST:
                self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                self.Tokens.advance()
            elif self.Tokens.symbol() in CompilationEngine.UNARY_OP:
                command = self.ARITHMATIC[self.Tokens.getToken()]
                self.vm_writer.writeArithmatic(command)
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileTerm()
            elif self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                if self.Tokens.symbol() in ["[", "("]:
                    if self.Tokens.symbol() == "[":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                        if self.Tokens.getToken() not in CompilationEngine.SET:
                            self.compileExpression()
                            if self.Tokens.symbol() == "]":
                                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                                self.Tokens.advance()
                    elif self.Tokens.symbol() == "(":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                        self.compileExpressionList()
                        if self.Tokens.symbol() == ")":
                            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                            self.Tokens.advance()
                elif self.Tokens.symbol() == ".":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "(":
                            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                            self.Tokens.advance()
                            self.compileExpressionList()
                            if self.Tokens.symbol() == ")":
                                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                                self.Tokens.advance()
            elif self.Tokens.symbol() == "(":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileExpression()
                    if self.Tokens.symbol() == ")":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()

    def compileExpressionList(self):
        if self.Tokens.getToken() not in CompilationEngine.SET and self.Tokens.getToken() != ")":
            self.compileExpression()
            while self.Tokens.symbol() == ",":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileExpression()


if __name__ == "__main__":

    V = VMWriter(filename)
    T = Tokenizer(filename)
    T.tokenize()
    E = CompilationEngine(tokens=T, vm_writer=V)
    S = SymbolTable()
    E.compileClass(symbol_table=S)
    V.close()

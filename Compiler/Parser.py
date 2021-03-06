import sys
from Tokenizer import Tokenizer
from SymbolTable import SymbolTable

class CompilationEngine:

    BINARY_OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    UNARY_OP = ["-", "~"]
    KEYWORD_CONST = ["true", "false", "null", "this"]
    SET = set(Tokenizer.KEYWORDS + Tokenizer.SYMBOLS) - set(["("] + BINARY_OP + KEYWORD_CONST)


    def __init__(self, filename, tokens, vm_writer):
        self.out_filename = filename.replace(".jack", ".xml")
        self.outfile = open(self.out_filename, "w")
        self.Tokens = tokens
        self.vm_writer = vm_writer

    def write(self, line):
        self.outfile.write(line)

    def close(self):
        self.outfile.close()

    def compileClass(self, symbol_table):
        self.Tokens.advance()
        if self.Tokens.keyWord() == "CLASS":
            self.write("<class>\n")
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
                        self.write("</class>\n")
        self.close()

    def compileClassVarDec(self, symbol_table):
        self.write("<classVarDec>\n")
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
                    self.write("</classVarDec>\n")

    def compileSubroutineDec(self, symbol_table):
        self.write("<SubroutineDec>\n")
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
                    if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                        self.compileParameterList(symbol_table=symbol_table)
                    #self.Tokens.advance()
                    if self.Tokens.symbol() == ")":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.compileSubroutineBody(symbol_table=symbol_table)
                            self.Tokens.advance()
                            self.write("</SubroutineDec>\n")

    def compileParameterList(self, symbol_table):
        self.write("<ParameterList>\n")
        var_kind = 'argument'   # variable kind
        if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
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
                    self.write("</ParameterList>\n")

    def compileSubroutineBody(self, symbol_table):
        self.write("<SubroutineBody>\n")
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
                self.write("</SubroutineBody>\n")

    def compileVarDec(self, symbol_table):
        self.write("<VarDec>\n")
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
                    self.write("</VarDec>\n")

    def compileStatements(self):
        self.write("<Statements>\n")
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
        self.write("</Statements>\n")

    def compileLet(self):
        self.write("<letStatement>\n")
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
                            self.write("</letStatement>\n")

    def compileDo(self):
        self.write("<doStatement>\n")
        if self.Tokens.keyWord() == "DO":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.symbol() != ";":
                self.compileExpression()
                if self.Tokens.symbol() == ";":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    self.write("</doStatement>\n")

    def compileIf(self):
        self.write("<ifStatement>\n")
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
                                self.write("</ifStatement>\n")

    def compileWhile(self):
        self.write("<whileStatement>\n")
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
                                    self.write("</whileStatement>\n")

    def compileReturn(self):
        self.write("<returnStatement>\n")
        if self.Tokens.keyWord() == "RETURN":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.symbol() != ";":
                self.compileExpression()
            if self.Tokens.symbol() == ";":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                self.write("</returnStatement>\n")

    def compileExpression(self):
        self.write("<Expression>\n")
        if self.Tokens.getToken() not in CompilationEngine.SET:
            self.compileTerm()
            while self.Tokens.getToken() not in CompilationEngine.SET:
                if self.Tokens.symbol() in CompilationEngine.BINARY_OP:
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.getToken() not in CompilationEngine.SET:
                        self.compileTerm()
                        self.write("</Expression>\n")

    def compileTerm(self):
        self.write("<term>\n")
        if self.Tokens.getToken() not in CompilationEngine.SET:
            if self.Tokens.tokenType() == "INT_CONST":
                self.write("<integerConstant> " + self.Tokens.getToken() + " </integerConstant>\n")
                self.Tokens.advance()
            elif self.Tokens.tokenType() == "STR_CONST":
                self.write("<stringConstant> " + self.Tokens.getToken() + " </stringConstant>\n")
                self.Tokens.advance()
            elif self.Tokens.keyWord() in CompilationEngine.KEYWORD_CONST:
                self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                self.Tokens.advance()
            elif self.Tokens.symbol() in CompilationEngine.UNARY_OP:
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
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
                        if self.Tokens.getToken() not in CompilationEngine.SET:
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
                            if self.Tokens.getToken() not in CompilationEngine.SET:
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
            self.write("</term>\n")

    def compileExpressionList(self):
        self.write("<ExpressionList>\n")
        if self.Tokens.getToken() not in CompilationEngine.SET:
            self.compileExpression()
            while self.Tokens.symbol() == ",":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileExpression()
        self.write("</ExpressionList>\n")


if __name__ == "__main__":

    C = CompilationEngine(sys.argv[1])
    S = SymbolTable()
    C.compileClass(symbol_table=S)

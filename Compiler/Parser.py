import sys
from Tokenizer import Tokenizer

class CompilationEngine:

    BINARY_OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    UNARY_OP = ["-", "~"]
    KEYWORD_CONST = ["true", "false", "null", "this"]
    SET = set(Tokenizer.KEYWORDS + Tokenizer.SYMBOLS) - set(["("] + BINARY_OP + KEYWORD_CONST)


    def __init__(self, filename):
        self.in_filename = filename
        self.out_filename = filename.replace(".jack", ".xml")
        self.outfile = open(self.out_filename, "w")
        self.Tokens = Tokenizer(self.in_filename)
        self.Tokens.tokenize()

    def write(self, line):
        self.outfile.write(line)

    def close(self):
        self.outfile.close()

    def compileClass(self):
        self.Tokens.advance()
        if self.Tokens.keyWord() == "CLASS":
            self.write("<class>\n")
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                #self.Tokens.identifier()
                self.Tokens.advance()
                if self.Tokens.symbol() == "{":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    while self.Tokens.keyWord() in ["STATIC", "FIELD"]:
                        self.compileClassVarDec()
                    while self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
                        self.compileSubroutineDec()
                    if self.Tokens.symbol() == "}":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.write("</class>\n")
        self.close()

    def compileClassVarDec(self):
        self.write("<classVarDec>\n")
        if self.Tokens.keyWord() in ["STATIC", "FIELD"]:
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            elif self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                while self.Tokens.symbol() == ",":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                        self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    self.write("</classVarDec>\n")

    def compileSubroutineDec(self):
        self.write("<SubroutineDec>\n")
        if self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
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
                        self.compileParameterList()
                    #self.Tokens.advance()
                    if self.Tokens.symbol() == ")":
                        self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.compileSubroutineBody()
                            self.Tokens.advance()
                            self.write("</SubroutineDec>\n")

    def compileParameterList(self):
        self.write("<ParameterList>\n")
        if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
        elif self.Tokens.tokenType() == "IDENTIFIER":
            self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
        self.Tokens.advance()
        if self.Tokens.tokenType() == "IDENTIFIER":
            self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
            while self.Tokens.symbol() == ",":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                    self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
                elif self.Tokens.tokenType() == "IDENTIFIER":
                    self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                if self.Tokens.tokenType() == "IDENTIFIER":
                    self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                    self.Tokens.advance()
                    self.write("</ParameterList>\n")

    def compileSubroutineBody(self):
        self.write("<SubroutineBody>\n")
        if self.Tokens.symbol() == "{":
            self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
            self.Tokens.advance()
            while self.Tokens.keyWord() == "VAR":
                self.compileVarDec()
            if self.Tokens.keyWord() in ["LET", "DO", "IF", "WHILE", "RETURN"]:
                self.compileStatements()
            if self.Tokens.symbol() == "}":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                self.write("</SubroutineBody>\n")

    def compileVarDec(self):
        self.write("<VarDec>\n")
        if self.Tokens.keyWord() == "VAR":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            elif self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                self.Tokens.advance()
                while self.Tokens.symbol() == ",":
                    self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
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
        self.write("<Term>\n")
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
            self.write("</Term>\n")

    def compileExpressionList(self):
        self.write("<ExpressionList>\n")
        if True:
            self.compileExpression()
            while self.Tokens.symbol() == ",":
                self.write("<symbol> " + self.Tokens.getToken() + " </symbol>\n")
                self.Tokens.advance()
                if True:
                    self.compileExpression()
        self.write("</ExpressionList>\n")


if __name__ == "__main__":

    C = CompilationEngine(sys.argv[1])
    C.compileClass()

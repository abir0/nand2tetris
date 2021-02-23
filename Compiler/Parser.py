import sys
from Tokenizer import Tokenizer

class CompilationEngine:

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
            self.compileType()
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
                    self.write("</classVarDec>\n")
                    self.Tokens.advance()

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
                        self.compileSubroutineBody()
                        self.write("</SubroutineDec>\n")
                        self.Tokens.advance()

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
                self.compileType()
                self.Tokens.advance()
                if self.Tokens.tokenType() == "IDENTIFIER":
                    self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")
                    self.write("</ParameterList>\n")
                    self.Tokens.advance()

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
                self.write("</SubroutineBody>\n")
                self.Tokens.advance()

    def compileVarDec(self):
        self.write("<VarDec>\n")
        if self.Tokens.keyWord() == "VAR":
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
            self.Tokens.advance()
            self.compileType()
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
                    self.write("</VarDec>\n")
                    self.Tokens.advance()

    def compileType(self):
        if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
            self.write("<keyword> " + self.Tokens.getToken() + " </keyword>\n")
        elif self.Tokens.tokenType() == "IDENTIFIER":
            self.write("<identifier> " + self.Tokens.getToken() + " </identifier>\n")

    def compileStatements(self):
        pass

    def compileLet(self):
        pass

    def compileDo(self):
        pass

    def compileIf(self):
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass


if __name__ == "__main__":

    C = CompilationEngine(sys.argv[1])
    C.compileClass()

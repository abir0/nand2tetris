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
        token = self.Tokens.advance()
        if self.Tokens.tokenType() == "KEYWORD" and self.Tokens.keyWord() == "CLASS":
            self.write("<class>\n")
            self.write("<keyword> " + token + " </keyword>\n")
            token = self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.write("<identifier> " + token + " </identifier>\n")
                #self.Tokens.identifier()
                token = self.Tokens.advance()
                if self.Tokens.tokenType() == "SYMBOL" and self.Tokens.symbol() == "{":
                    self.write("<symbol> " + token + " </symbol>\n")
                    token = self.Tokens.advance()
                    self.compileClassVarDec()
                    self.compileSubroutineDec()
                    if self.Tokens.tokenType() == "SYMBOL" and self.Tokens.symbol() == "}":
                        self.write("<symbol> " + token + " </symbol>\n")
                        self.write("</class>")
        self.close()

    def compileClassVarDec(self):
        pass

    def compileSubroutineDec(self):
        pass

    def compileParameterList(self):
        pass

    def compileSubroutineBody(self):
        pass

    def compileVarDec(self):
        pass

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

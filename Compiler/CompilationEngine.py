import sys
from Tokenizer import Tokenizer
from SymbolTable import SymbolTable

class CompilationEngine:


    ARITHMATIC_MAP = {"+" : "add", "-" : "sub", "*" : "Math.multiply",
                  "/" : "Math.divide", "&" : "and", "|" : "or", "<" : "lt",
                  ">" : "gt", "=" : "eq", "-" : "neg", "~" : "not"}

    SEGMENT_MAP = {"field" : "this", "static" : "static", "var" : "local", "arg" : "argument"}

    BINARY_OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    UNARY_OP = ["-", "~"]

    KEYWORD_CONST = ["true", "false", "null", "this"]

    SET = set(Tokenizer.KEYWORDS + Tokenizer.SYMBOLS) - set(["("] + UNARY_OP + BINARY_OP + KEYWORD_CONST)


    def __init__(self, tokens, vm_writer, symbol_table, verbose=False):
        self.Tokens = tokens
        self.vm_writer = vm_writer
        self.symbol_table = symbol_table
        self.label = 0
        self.verbose = verbose


    def compileClass(self):
        self.Tokens.advance()
        if self.Tokens.keyWord() == "CLASS":
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                class_name = self.Tokens.getToken()
                self.Tokens.advance()
                if self.Tokens.symbol() == "{":
                    self.Tokens.advance()
                    while self.Tokens.keyWord() in ["STATIC", "FIELD"]:
                        self.compileClassVarDec()
                    while self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
                        self.symbol_table.startSubroutine()
                        if self.Tokens.keyWord() != "FUNCTION":
                            self.symbol_table.define(name='this', kind='argument', type=class_name)
                        self.compileSubroutineDec(class_name)
                    if self.Tokens.symbol() == "}":
                        pass


    def compileClassVarDec(self):
        if self.Tokens.keyWord() in ["STATIC", "FIELD"]:
            var_kind = self.SEGMENT_MAP[self.Tokens.getToken()]
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                var_type = self.Tokens.getToken()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                    pass
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                var_name = self.Tokens.getToken()
                self.symbol_table.define(name=var_name, type=var_type, kind=var_kind, class_flag=True)
                self.Tokens.advance()
                while self.Tokens.symbol() == ",":
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        var_name = self.Tokens.getToken()
                        self.symbol_table.define(name=var_name, type=var_type, kind=var_kind, class_flag=True)
                        self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.Tokens.advance()


    def compileSubroutineDec(self, class_name):
        nLocals = self.symbol_table.varCount("this", class_flag=True)
        if nLocals == -1:
            nLocals = 0
        if self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
            name = self.Tokens.getToken()
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["VOID", "INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                if self.Tokens.keyWord() == "VOID":
                    ##################################
                    ##### VOID handling needed #######
                    ##################################
                    pass
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                func_name = self.Tokens.getToken()
                if name == "function":
                    kind = class_name
                else:
                    kind = self.symbol_table.KindOf(func_name)
                func_name = kind + "." + func_name
                self.Tokens.advance()
                if self.Tokens.symbol() == "(":
                    self.Tokens.advance()
                    self.compileParameterList()
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            if name == "constructor":
                                self.vm_writer.writeFunction(func_name, str(nLocals))
                                ### Object construction ###
                                self.vm_writer.writePush("constant", str(nLocals))
                                self.vm_writer.writeCall("Memory.alloc", "1")
                                self.vm_writer.writePop("pointer", "0")
                            elif name == "method":
                                self.vm_writer.writeFunction(func_name, str(nLocals))
                                ### Method construction ###
                                self.vm_writer.writePush("argument", "0")
                                self.vm_writer.writePop("pointer", "0")
                            elif name == "function":
                                self.vm_writer.writeFunction(func_name, str(nLocals))
                            self.compileSubroutineBody()


    def compileParameterList(self):
        if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
            var_kind = self.SEGMENT_MAP["arg"]   # variable kind
            var_type = self.Tokens.getToken()   # variable type
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                pass
            elif self.Tokens.tokenType() == "IDENTIFIER":
                pass
            self.Tokens.advance()
        if self.Tokens.tokenType() == "IDENTIFIER":
            var_name = self.Tokens.getToken()   # variable name
            self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)    # define variable
            self.Tokens.advance()
            while self.Tokens.symbol() == ",":
                self.Tokens.advance()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                    var_type = self.Tokens.getToken()
                    if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                        pass
                self.Tokens.advance()
                if self.Tokens.tokenType() == "IDENTIFIER":
                    var_name = self.Tokens.getToken()
                    self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                    self.Tokens.advance()


    def compileSubroutineBody(self):
        if self.Tokens.symbol() == "{":
            self.Tokens.advance()
            while self.Tokens.keyWord() == "VAR":
                self.compileVarDec()
            if self.Tokens.keyWord() in ["LET", "DO", "IF", "WHILE", "RETURN"]:
                self.compileStatements()
            if self.Tokens.symbol() == "}":
                self.Tokens.advance()


    def compileVarDec(self):
        if self.Tokens.keyWord() == "VAR":
            var_kind = self.SEGMENT_MAP[self.Tokens.getToken()]
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                var_type = self.Tokens.getToken()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"]:
                    pass
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                var_name = self.Tokens.getToken()
                self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                self.Tokens.advance()
                while self.Tokens.symbol() == ",":
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        var_name = self.Tokens.getToken()
                        self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                        self.Tokens.advance()
                if self.Tokens.symbol() == ";":
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
        array_flag = False
        if self.Tokens.keyWord() == "LET":
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                name = self.Tokens.getToken()
                segment = self.symbol_table.KindOf(name)
                index = self.symbol_table.IndexOf(name)
                self.Tokens.advance()
                if self.Tokens.symbol() == "[":
                    self.Tokens.advance()
                    if self.Tokens.symbol() != "]":
                        self.compileExpression()
                        self.vm_writer.writePush(segment, str(index))
                        if self.Tokens.symbol() == "]":
                            self.vm_writer.writeArithmatic("add")
                            array_flag = True
                            self.Tokens.advance()
                if self.Tokens.symbol() == "=":
                    self.Tokens.advance()
                    if self.Tokens.symbol() != ";":
                        self.compileExpression()
                        if array_flag:
                            self.vm_writer.writePop("temp", "0")
                            self.vm_writer.writePop("pointer", "1")
                            self.vm_writer.writePush("temp", "0")
                            self.vm_writer.writePop("that", "0")
                        else:
                            self.vm_writer.writePop(segment, str(index))
                        if self.Tokens.symbol() == ";":
                            self.Tokens.advance()


    def compileDo(self):
        if self.Tokens.keyWord() == "DO":
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                name = self.Tokens.getToken()
                self.Tokens.advance()
                if self.Tokens.symbol() == "(":
                    self.Tokens.advance()
                    nArgs = self.compileExpressionList()
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                elif self.Tokens.symbol() == ".":
                    name += "."
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        name +=  self.Tokens.getToken()
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "(":
                            self.Tokens.advance()
                            nArgs = self.compileExpressionList()
                            if self.Tokens.symbol() == ")":
                                self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.Tokens.advance()
                    self.vm_writer.writeCall(name, str(nArgs))
                    self.vm_writer.writePop("temp", "0")


    def compileIf(self):
        labels = []
        if self.Tokens.keyWord() == "IF":
            self.Tokens.advance()
            if self.Tokens.symbol() == "(":
                self.Tokens.advance()
                if self.Tokens.symbol() != ")":
                    self.compileExpression()
                    self.vm_writer.writeArithmatic("not")
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.Tokens.advance()
                            if self.Tokens.symbol() != "}":
                                labels.append(self.generateLabel())
                                self.vm_writer.writeIf(labels[-1])
                                self.compileStatements()
                                if self.Tokens.symbol() == "}":
                                    self.Tokens.advance()
                                if self.Tokens.keyWord() == "ELSE":
                                    self.Tokens.advance()
                                    if self.Tokens.symbol() == "{":
                                        self.Tokens.advance()
                                        if self.Tokens.symbol() != "}":
                                            labels.append(self.generateLabel())
                                            self.vm_writer.writeGoto(labels[-1])
                                            self.vm_writer.writeLabel(labels.pop(0))
                                            self.compileStatements()
                                            if self.Tokens.symbol() == "}":
                                                self.Tokens.advance()
                                self.vm_writer.writeLabel(labels.pop(0))


    def compileWhile(self):
        labels = []
        if self.Tokens.keyWord() == "WHILE":
            self.Tokens.advance()
            if self.Tokens.symbol() == "(":
                self.Tokens.advance()
                if self.Tokens.symbol() != ")":
                    labels.append(self.generateLabel())
                    self.vm_writer.writeLabel(labels[-1])
                    self.compileExpression()
                    self.vm_writer.writeArithmatic("not")
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.Tokens.advance()
                            if self.Tokens.symbol() != "}":
                                labels.append(self.generateLabel())
                                self.vm_writer.writeIf(labels[-1])
                                self.compileStatements()
                                self.vm_writer.writeGoto(labels.pop(0))
                                if self.Tokens.symbol() == "}":
                                    self.Tokens.advance()
                                    self.vm_writer.writeLabel(labels.pop(0))


    def compileReturn(self):
        if self.Tokens.keyWord() == "RETURN":
            self.Tokens.advance()
            if self.Tokens.symbol() != ";":
                self.compileExpression()
            else:
                self.vm_writer.writePush("constant", "0")
            if self.Tokens.symbol() == ";":
                self.vm_writer.writeReturn()
                self.Tokens.advance()


    def compileExpression(self):
        if self.Tokens.getToken() not in CompilationEngine.SET:
            self.compileTerm()
            while self.Tokens.getToken() not in CompilationEngine.SET:
                if self.Tokens.symbol() in CompilationEngine.BINARY_OP:
                    call = False
                    if self.Tokens.getToken() in ["*", "/"]:
                        call = True
                    command = self.ARITHMATIC_MAP[self.Tokens.getToken()]
                    self.Tokens.advance()
                    if self.Tokens.getToken() not in CompilationEngine.SET:
                        self.compileTerm()
                        if not call:
                            self.vm_writer.writeArithmatic(command)
                        else:
                            self.vm_writer.writeCall(command, "2")


    def compileTerm(self):
        if self.Tokens.getToken() not in CompilationEngine.SET:
            if self.Tokens.tokenType() == "INT_CONST":
                self.vm_writer.writePush("constant", self.Tokens.getToken())
                self.Tokens.advance()
            elif self.Tokens.tokenType() == "STR_CONST":
                string = self.Tokens.getToken()[1:-1]
                length = len(string)
                self.vm_writer.writePush("constant", str(length))
                self.vm_writer.writeCall("String.new", "1")
                for i in string:
                    self.vm_writer.writePush("constant", str(ord(i)))
                    self.vm_writer.writeCall("String.appendChar", "2")
                self.Tokens.advance()
            elif self.Tokens.getToken() in CompilationEngine.KEYWORD_CONST:
                ### Keyword constant ###
                if self.Tokens.getToken() == "this":
                    self.vm_writer.writePush("pointer", "0")
                elif self.Tokens.getToken() in ["false", "null"]:
                    self.vm_writer.writePush("constant", "0")
                elif self.Tokens.getToken() == "true":
                    self.vm_writer.writePush("constant", "1")
                    self.vm_writer.writeArithmatic("neg")
                self.Tokens.advance()
            elif self.Tokens.symbol() in CompilationEngine.UNARY_OP:
                command = self.ARITHMATIC_MAP[self.Tokens.getToken()]
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileTerm()
                    self.vm_writer.writeArithmatic(command)
            elif self.Tokens.tokenType() == "IDENTIFIER":
                name = self.Tokens.getToken()
                self.Tokens.advance()
                if self.Tokens.symbol() not in ["[", "(", "."]:
                    segment = self.symbol_table.KindOf(name)
                    index = self.symbol_table.IndexOf(name)
                    self.vm_writer.writePush(segment, str(index))
                if self.Tokens.symbol() == "[":
                    segment = self.symbol_table.KindOf(name)
                    index = self.symbol_table.IndexOf(name)
                    self.Tokens.advance()
                    if self.Tokens.getToken() not in CompilationEngine.SET:
                        self.compileExpression()
                        self.vm_writer.writePush(segment, str(index))
                        if self.Tokens.symbol() == "]":
                            self.vm_writer.writeArithmatic("add")
                            self.vm_writer.writePop("pointer", "1")
                            self.vm_writer.writePush("that", "0")
                            self.Tokens.advance()
                elif self.Tokens.symbol() == "(":
                    self.Tokens.advance()
                    ### Subroutine call ###
                    nArgs = self.compileExpressionList()
                    self.vm_writer.writeCall(name, str(nArgs))
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                elif self.Tokens.symbol() == ".":
                    name = self.symbol_table.KindOf(name)
                    name += self.Tokens.getToken()
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        name += self.Tokens.getToken()
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "(":
                            self.Tokens.advance()
                            nArgs = self.compileExpressionList()
                            if self.Tokens.symbol() == ")":
                                self.Tokens.advance()
                                ### Class.Subroutine call ###
                                self.vm_writer.writeCall(name, str(nArgs))
            elif self.Tokens.symbol() == "(":
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileExpression()
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()


    def compileExpressionList(self):
        count = 0
        if self.Tokens.getToken() not in CompilationEngine.SET and self.Tokens.getToken() != ")":
            self.compileExpression()
            count += 1
            while self.Tokens.symbol() == ",":
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileExpression()
                    count += 1
        return count


    def generateLabel(self):
        self.label += 1
        return "L" + str(self.label)


if __name__ == "__main__":

    V = VMWriter(filename)
    T = Tokenizer(filename)
    T.tokenize()
    S = SymbolTable()
    E = CompilationEngine(tokens=T, vm_writer=V, symbol_table=S)
    E.compileClass()
    V.close()

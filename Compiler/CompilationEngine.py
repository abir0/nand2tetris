import sys
from Tokenizer import Tokenizer
from SymbolTable import SymbolTable

class CompilationEngine:


    # Maps arithmatic symbols to corresponding VM command
    ARITHMATIC_MAP = {"+" : "add", "-" : "sub", "*" : "Math.multiply",
                  "/" : "Math.divide", "&" : "and", "|" : "or", "<" : "lt",
                  ">" : "gt", "=" : "eq", "-" : "sub"}

    UNARY_MAP = {"-" : "neg", "~" : "not"}

    # Jack operators and keyword constants
    BINARY_OP = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    UNARY_OP = ["-", "~"]

    KEYWORD_CONST = ["true", "false", "null", "this"]

    # This set includes all keywords and symbols except those above
    SET = set(Tokenizer.KEYWORDS + Tokenizer.SYMBOLS) - set(["("] + UNARY_OP + BINARY_OP + KEYWORD_CONST)


    def __init__(self, tokens, vm_writer, symbol_table, verbose=False):
        self.Tokens = tokens
        self.vm_writer = vm_writer
        self.symbol_table = symbol_table
        self.label = -1  # for unique label generation
        self.verbose = verbose


    def compileClass(self):
        """Compile Jack class and generate code from top to down."""
        self.Tokens.advance()
        if self.Tokens.keyWord() == "CLASS":
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                self.class_name = self.Tokens.getToken()
                self.Tokens.advance()
                if self.Tokens.symbol() == "{":
                    self.Tokens.advance()
                    while self.Tokens.keyWord() in ["STATIC", "FIELD"]:
                        self.compileClassVarDec()
                    while self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
                        self.symbol_table.startSubroutine()
                        if self.Tokens.keyWord() == "METHOD":
                            self.symbol_table.define(name='this', kind='argument', type=self.class_name)
                        self.compileSubroutineDec()
                    if self.Tokens.symbol() == "}":
                        print("Compiled {} class successfully".format(self.class_name))


    def compileClassVarDec(self):
        """Compile class variable declaration and update symbol table."""
        if self.Tokens.keyWord() in ["STATIC", "FIELD"]:
            var_kind = self.Tokens.getToken().replace("field", "this")
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                var_type = self.Tokens.getToken()
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


    def compileSubroutineDec(self):
        """Compile subroutine declaration and generate code top to down."""
        if self.Tokens.keyWord() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]:
            func_type = self.Tokens.getToken()
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["VOID", "INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                if self.Tokens.keyWord() == "VOID":
                    ###########################
                    ### VOID type handling  ###
                    ###########################
                    pass
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                func_name = self.Tokens.getToken()
                func_name = self.class_name + "." + func_name
                self.Tokens.advance()
                if self.Tokens.symbol() == "(":
                    self.Tokens.advance()
                    self.compileParameterList()
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.compileSubroutineBody(func_type, func_name)


    def compileParameterList(self):
        """Compile subroutine parameter list and update symbol table."""
        if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
            var_kind = "argument"   # variable kind
            var_type = self.Tokens.getToken()   # variable type
            self.Tokens.advance()
        if self.Tokens.tokenType() == "IDENTIFIER":
            var_name = self.Tokens.getToken()   # variable name
            self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)    # define variable
            self.Tokens.advance()
            while self.Tokens.symbol() == ",":
                self.Tokens.advance()
                if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                    var_type = self.Tokens.getToken()
                self.Tokens.advance()
                if self.Tokens.tokenType() == "IDENTIFIER":
                    var_name = self.Tokens.getToken()
                    self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                    self.Tokens.advance()


    def compileSubroutineBody(self, func_type, func_name):
        """Compile subroutine body section and generate code."""
        if self.Tokens.symbol() == "{":
            self.Tokens.advance()
            count = 0
            while self.Tokens.keyWord() == "VAR":
                count += self.compileVarDec()
            nLocals = count
            if func_type == "constructor":
                self.vm_writer.writeFunction(func_name, str(nLocals))
                ### Object construction ###
                nArgs = self.symbol_table.varCount("this", class_flag=True)
                self.vm_writer.writePush("constant", str(nArgs))
                self.vm_writer.writeCall("Memory.alloc", "1")
                self.vm_writer.writePop("pointer", "0")
            elif func_type == "method":
                self.vm_writer.writeFunction(func_name, str(nLocals))
                ### Method construction ###
                self.vm_writer.writePush("argument", "0")
                self.vm_writer.writePop("pointer", "0")
            elif func_type == "function":
                self.vm_writer.writeFunction(func_name, str(nLocals))
            if self.Tokens.keyWord() in ["LET", "DO", "IF", "WHILE", "RETURN"]:
                self.compileStatements()
            if self.Tokens.symbol() == "}":
                self.Tokens.advance()


    def compileVarDec(self):
        """Compile local variable declaration list and update symbol table."""
        count = 0
        if self.Tokens.keyWord() == "VAR":
            var_kind = "local"
            self.Tokens.advance()
            if self.Tokens.keyWord() in ["INT", "CHAR", "BOOLEAN"] or self.Tokens.tokenType() == "IDENTIFIER":
                var_type = self.Tokens.getToken()
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                var_name = self.Tokens.getToken()
                self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                count += 1
                self.Tokens.advance()
                while self.Tokens.symbol() == ",":
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        var_name = self.Tokens.getToken()
                        self.symbol_table.define(name=var_name, type=var_type, kind=var_kind)
                        count += 1
                        self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.Tokens.advance()
        return count


    def compileStatements(self):
        """Compile statements and generate code recursively."""
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
        """Compile let statement and generate code."""
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
        """Compile do statement and generate code."""
        if self.Tokens.keyWord() == "DO":
            self.Tokens.advance()
            if self.Tokens.tokenType() == "IDENTIFIER":
                name = self.Tokens.getToken()
                method_call = False
                self.Tokens.advance()
                if self.Tokens.symbol() == "(":
                    self.Tokens.advance()
                    func_name = self.class_name + "." + name
                    method_call = True
                    self.vm_writer.writePush("pointer", "0")
                    nArgs = self.compileExpressionList()
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                elif self.Tokens.symbol() == ".":
                    func_name = self.symbol_table.TypeOf(name)
                    method_call = False
                    if name != func_name:
                        segment = self.symbol_table.KindOf(name)
                        index = self.symbol_table.IndexOf(name)
                        self.vm_writer.writePush(segment, str(index))
                        method_call = True
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        func_name = func_name + "." +  self.Tokens.getToken()
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "(":
                            self.Tokens.advance()
                            nArgs = self.compileExpressionList()
                            if self.Tokens.symbol() == ")":
                                self.Tokens.advance()
                if self.Tokens.symbol() == ";":
                    self.Tokens.advance()
                    if method_call:
                        self.vm_writer.writeCall(func_name, str(nArgs + 1))
                    else:
                        self.vm_writer.writeCall(func_name, str(nArgs))
                    self.vm_writer.writePop("temp", "0")


    def compileIf(self):
        """Compile if statement and generate code recursively."""
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
                                labels.append(self.generateLabel("IF_TRUE"))
                                self.vm_writer.writeIf(labels[-1])
                                self.compileStatements()
                                if self.Tokens.symbol() == "}":
                                    self.Tokens.advance()
                                if self.Tokens.keyWord() == "ELSE":
                                    self.Tokens.advance()
                                    if self.Tokens.symbol() == "{":
                                        self.Tokens.advance()
                                        if self.Tokens.symbol() != "}":
                                            labels.append(self.generateLabel("IF_FALSE"))
                                            self.vm_writer.writeGoto(labels[-1])
                                            self.vm_writer.writeLabel(labels.pop(0))
                                            self.compileStatements()
                                            if self.Tokens.symbol() == "}":
                                                self.Tokens.advance()
                                self.vm_writer.writeLabel(labels.pop(0))


    def compileWhile(self):
        """Compile while statement and generate code recursively."""
        labels = []
        if self.Tokens.keyWord() == "WHILE":
            self.Tokens.advance()
            if self.Tokens.symbol() == "(":
                self.Tokens.advance()
                if self.Tokens.symbol() != ")":
                    labels.append(self.generateLabel("WHILE_EXP"))
                    self.vm_writer.writeLabel(labels[-1])
                    self.compileExpression()
                    self.vm_writer.writeArithmatic("not")
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "{":
                            self.Tokens.advance()
                            if self.Tokens.symbol() != "}":
                                labels.append(self.generateLabel("WHILE_END"))
                                self.vm_writer.writeIf(labels[-1])
                                self.compileStatements()
                                self.vm_writer.writeGoto(labels.pop(0))
                                if self.Tokens.symbol() == "}":
                                    self.Tokens.advance()
                                    self.vm_writer.writeLabel(labels.pop(0))


    def compileReturn(self):
        """Compile return statement and generate code."""
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
        """Compile expression and generate code recursively."""
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
        """Compile term and generate code recursively."""
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
                    self.vm_writer.writePush("constant", "0")
                    self.vm_writer.writeArithmatic("not")
                self.Tokens.advance()
            elif self.Tokens.symbol() in CompilationEngine.UNARY_OP:
                command = self.UNARY_MAP[self.Tokens.getToken()]
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
                    func_name = self.class_name + "." + name
                    nArgs = self.compileExpressionList()
                    self.vm_writer.writeCall(func_name, str(nArgs))
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()
                elif self.Tokens.symbol() == ".":
                    func_name = self.symbol_table.TypeOf(name)
                    method_call = False
                    if name != func_name:
                        segment = self.symbol_table.KindOf(name)
                        index = self.symbol_table.IndexOf(name)
                        self.vm_writer.writePush(segment, str(index))
                        method_call = True
                        #self.vm_writer.writePush("pointer", "0")
                    self.Tokens.advance()
                    if self.Tokens.tokenType() == "IDENTIFIER":
                        func_name = func_name + "." +  self.Tokens.getToken()
                        self.Tokens.advance()
                        if self.Tokens.symbol() == "(":
                            self.Tokens.advance()
                            nArgs = self.compileExpressionList()
                            if self.Tokens.symbol() == ")":
                                self.Tokens.advance()
                                ### Class.Subroutine call ###
                                if method_call:
                                    self.vm_writer.writeCall(func_name, str(nArgs + 1))
                                else:
                                    self.vm_writer.writeCall(func_name, str(nArgs))
            elif self.Tokens.symbol() == "(":
                self.Tokens.advance()
                if self.Tokens.getToken() not in CompilationEngine.SET:
                    self.compileExpression()
                    if self.Tokens.symbol() == ")":
                        self.Tokens.advance()


    def compileExpressionList(self):
        """Compile expression list and generate code recursively."""
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


    def generateLabel(self, prefix):
        """Generate unique labels for if and while statements."""
        self.label += 1
        return prefix + str(self.label)


if __name__ == "__main__":

    V = VMWriter(filename)
    T = Tokenizer(filename)
    T.tokenize()
    S = SymbolTable()
    E = CompilationEngine(tokens=T, vm_writer=V, symbol_table=S)
    E.compileClass()
    V.close()

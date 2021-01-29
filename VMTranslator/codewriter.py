import sys, re

class CodeWriter:
    """Take parsed VM code and write assembly code into new file."""

    # Segment names in assembly language
    SEGMENT_NAME = {
        "local" : "LCL",
        "argument" : "ARG",
        "this" : "THIS",
        "that" : "THAT"
    }

    # Assembly mapping of arithmatic commands
    ARITHMATIC_MAP = {
            "add" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n",
            "sub" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n",
            "neg" : "@SP\nA=M-1\nM=-M\n",
            "and" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n",
            "or" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n",
            "not" : "@SP\nA=M-1\nM=!M\n",
            "eq" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_EQ{i}\nD;JNE\n@SP\nA=M-1\nM=-1\n(END_EQ{i})\n",
            "gt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_GT{i}\nD;JLE\n@SP\nA=M-1\nM=-1\n(END_GT{i})\n",
            "lt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_LT{i}\nD;JGE\n@SP\nA=M-1\nM=-1\n(END_LT{i})\n"
    }

    # Assembly mapping of memory segment commands
    PUSHPOP_MAP = {
            "push segment" : "@{i}\nD=A\n@{segment}\nA=M+D\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop segment" : "@{i}\nD=A\n@{segment}\nAD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "push temp" : "@{i}\nD=A\n@5\nA=A+D\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop temp" : "@{i}\nD=A\n@5\nAD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "push constant" : "@{i}\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "push pointer" : "@{pointer}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop pointer" : "@SP\nAM=M-1\nD=M\n@{pointer}\nM=D\n",
            "push static" : "@{filename}.{i}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop static" : "@SP\nAM=M-1\nD=M\n@{filename}.{i}\nM=D\n"
    }


    def __init__(self, filename):
        self.filename = str(filename)
        self.filename = re.sub(r".vm$", "", self.filename)
        self.filename = re.sub(r"^\.\\", "", self.filename)
        self.filename = re.sub(r"\\$", "", self.filename)
        self.outfile = open(self.filename + ".asm", "w")
        self.outfile.write("// Translation of {} file\n".format(self.filename + ".asm"))
        self.jump_count = 0     # count the jump commands
        self.addr_count = 0


    def writeArithmatic(self, command):
        """Write arithmatic codes into file."""
        if command in ["eq", "gt", "lt"]:
            code = CodeWriter.ARITHMATIC_MAP[command]
            code = code.format(i=self.jump_count)
            self.outfile.write(code)
            self.jump_count += 1    # increament the count
        else:
            code = CodeWriter.ARITHMATIC_MAP[command]
            self.outfile.write(code)

    def writePushPop(self, command, segment, index):
        """Write memory segment codes into file."""
        if segment in CodeWriter.SEGMENT_NAME:
            code = CodeWriter.PUSHPOP_MAP[command + " " + "segment"]
            code = code.format(i=str(index), segment=CodeWriter.SEGMENT_NAME[segment])
            self.outfile.write(code)

        elif segment == "temp":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i=str(index))
            self.outfile.write(code)

        elif segment == "constant":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i=str(index))
            self.outfile.write(code)

        elif segment == "pointer":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(pointer=str(3 + int(index)))
            self.outfile.write(code)

        elif segment == "static":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(filename=self.filename, i=str(index))
            self.outfile.write(code)

    def writeLabel(self, label):
        self.outfile.write("({label})\n".format(label=label))
        self.outfile.write("@SP\nM=M-1\n")

    def writeGoto(self, label):
        self.outfile.write("@{label}\n".format(label=label))
        self.outfile.write("0;JMP\n")

    def writeIfgoto(self, label):
        self.outfile.write("D=M\n")
        self.outfile.write("@{label}\n".format(label=label))
        self.outfile.write("D;JNE\n")

    def writeFunction(self, functionName, nVars):
        self.outfile.write("({file}.{function})\n".format(file=self.filename, function=functionName))
        for num in range(int(nVars)):
            push = CodeWriter.PUSHPOP_MAP["push constant"]
            self.outfile.write(push.format(i="0"))

    def writeReturn(self):
        self.outfile.write("@LCL\nD=M\n@5\nA=D-A\nD=M\n@R13\nM=D\n")
        self.outfile.write("@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\nD=A+1\n@SP\nM=D\n")
        self.outfile.write("@LCL\nAM=M-1\nD=M\n@THAT\nM=D\n")
        self.outfile.write("@LCL\nAM=M-1\nD=M\n@THIS\nM=D\n")
        self.outfile.write("@LCL\nAM=M-1\nD=M\n@ARG\nM=D\n")
        self.outfile.write("@LCL\nA=M-1\nD=M\n@LCL\nM=D\n")
        self.outfile.write("@R13\nA=M\n0;JMP\n")

    def writeCall(self, functionName, nArgs):
        self.outfile.write("@SP\nD=M\n@R13\nM=D\n")
        self.outfile.write("@return.{i}\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n".format(i=self.addr_count))
        for i in ["LCL", "ARG", "THIS", "THAT"]:
            self.outfile.write("@{segment}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n".format(segment=i))
        self.outfile.write("\n@{args}\nD=A\n@5\nD=A+D\n@R13\nD=M-D\n@ARG\nM=D\n".format(args=nArgs))
        self.outfile.write("@SP\nD=M\n@LCL\nM=D\n")
        self.outfile.write("@{file}.{function}\n".format(file=self.filename, function=functionName))
        self.outfile.write("(return.{i})\n".format(i=self.addr_count))
        self.addr_count += 1

    def writeComment(self, line):
        """Write VM commands as comment into file."""
        self.outfile.write("  //" + line + "\n")

    def close(self):
        self.outfile.close()    # close file


if __name__ == "__main__":

    C = CodeWriter("Test_cases")

    # Test cases
    C.writeComment("label TEST_LABEL")
    C.writeLabel("TEST_LABEL")
    C.writeComment("push local 1")
    C.writePushPop("push", "local", "1")
    C.writeComment("push argument 0")
    C.writePushPop("push", "argument", "0")
    C.writeComment("add")
    C.writeArithmatic("add")
    C.writeComment("if-goto TEST_LABEL")
    C.writeIfgoto("TEST_LABEL")
    C.writeComment("pop static 1")
    C.writePushPop("pop", "static", "1")
    C.writeComment("goto TEST_LABEL")
    C.writeGoto("TEST_LABEL")

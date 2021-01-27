import sys

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
            "eq" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_EQ_{i}\nD;JNE\n@SP\nA=M-1\nM=-1\n(END_EQ_{i})\n",
            "gt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_GT_{i}\nD;JLE\n@SP\nA=M-1\nM=-1\n(END_GT_{i})\n",
            "lt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_LT_{i}\nD;JGE\n@SP\nA=M-1\nM=-1\n(END_LT_{i})\n"
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
        self.filename = filename.replace(".vm", "").replace(".\\", "")
        self.outfile = open(self.filename + ".asm", "w")
        self.outfile.write("// Translation of {} file\n".format(self.filename + ".asm"))
        self.jump_count = 0     # count the jump commands


    def writeArithmatic(self, command):
        """Write arithmatic codes into file."""
        if command in ["eq", "gt", "lt"]:
            code = CodeWriter.ARITHMATIC_MAP[command]
            code = code.format(i = self.jump_count)
            self.outfile.write(code)
            self.jump_count += 1    # increament the count
        else:
            code = CodeWriter.ARITHMATIC_MAP[command]
            self.outfile.write(code)

    def writePushPop(self, command, segment, index):
        """Write memory segment codes into file."""
        if segment in CodeWriter.SEGMENT_NAME:
            code = CodeWriter.PUSHPOP_MAP[command + " " + "segment"]
            code = code.format(i = str(index), segment = CodeWriter.SEGMENT_NAME[segment])
            self.outfile.write(code)

        elif segment == "temp":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i = str(index))
            self.outfile.write(code)

        elif segment == "constant":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i = str(index))
            self.outfile.write(code)

        elif segment == "pointer":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(pointer = str(3 + int(index)))
            self.outfile.write(code)

        elif segment == "static":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(filename = self.filename, i = str(index))
            self.outfile.write(code)

    def writeLabel(self, arg1):
        self.outfile.write("(" + arg1 + ")\n")
        self.outfile.write("@SP\nM=M-1\n")

    def writeGoto(self, arg1):
        self.outfile.write("@" + arg1 + "\n")
        self.outfile.write("0;JMP\n")

    def writeIfgoto(self, arg1):
        self.outfile.write("D=M\n")
        self.outfile.write("@" + arg1 + "\n")
        self.outfile.write("D;JNE\n")

    def writeFunction(self):
        pass

    def writeReturn(self):
        pass

    def writeCall(self):
        pass

    def writeComment(self, line):
        """Write VM commands as comment into file."""
        self.outfile.write("  //" + line + "\n")

    def close(self):
        self.outfile.close()    # close file


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: .\CodeWriter.py <filename>")
        sys.exit(1)

    C = CodeWriter(sys.argv[1])

    # Test cases
    for i in ["push", "pop"]:
        for j in ["local", "argument", "this", "that", "temp", "pointer", "static"]:
            for k in ["0", "1"]:
                C.writeComment(i + " " + j + " " + k)
                C.writePushPop(i, j, k)

    for i in ["add", "sub", "neg", "and", "or", "not", "eq", "lt", "gt", "eq", "lt", "gt"]:
        C.writeComment(i)
        C.writeArithmatic(i)

    C.writeComment("label TEST_LABEL")
    C.writeLabel("TEST_LABEL")
    C.writeComment("goto TEST_LABEL")
    C.writeGoto("TEST_LABEL")
    C.writeComment("if-goto TEST_LABEL")
    C.writeIfgoto("TEST_LABEL")

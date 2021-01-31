

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
            "eq" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_{i}\nD;JNE\n@SP\nA=M-1\nM=-1\n(END_{i})\n",
            "gt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_{i}\nD;JLE\n@SP\nA=M-1\nM=-1\n(END_{i})\n",
            "lt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_{i}\nD;JGE\n@SP\nA=M-1\nM=-1\n(END_{i})\n"
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
        self.filename = filename
        self.outfile = open(self.filename + ".asm", "a")
        self.outfile.write("// Translation of {} file\n".format(self.filename + ".asm"))
        self.jump_count = 0     # count the jump commands
        self.call_count = 0

    def write(self, command):
        self.outfile.write(command)

    def writeArithmatic(self, command):
        """Write arithmatic codes into file."""
        if command in ["eq", "gt", "lt"]:
            code = CodeWriter.ARITHMATIC_MAP[command]
            code = code.format(i=self.jump_count)
            self.write(code)
            self.jump_count += 1    # increment the count
        else:
            code = CodeWriter.ARITHMATIC_MAP[command]
            self.write(code)

    def writePushPop(self, command, segment, index):
        """Write memory segment codes into file."""
        if segment in CodeWriter.SEGMENT_NAME:
            code = CodeWriter.PUSHPOP_MAP[command + " " + "segment"]
            code = code.format(i=str(index), segment=CodeWriter.SEGMENT_NAME[segment])
            self.write(code)

        elif segment == "temp":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i=str(index))
            self.write(code)

        elif segment == "constant":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i=str(index))
            self.write(code)

        elif segment == "pointer":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(pointer=str(3 + int(index)))
            self.write(code)

        elif segment == "static":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(filename=self.filename, i=str(index))
            self.write(code)

    def writeLabel(self, label):
        # label
        self.write("({label})\n".format(label=label))

    def writeGoto(self, label):
        # goto label
        self.write("@{label}\n0;JMP\n".format(label=label))

    def writeIfgoto(self, label):
        # pop value
        self.write("@SP\nAM=M-1\nD=M\n")
        # goto label
        self.write("@{label}\nD;JNE\n".format(label=label))

    def writeFunction(self, functionName, nVars):
        # label functionName
        self.write("({function_name})\n".format(function_name=functionName))
        # push 0's
        self.write("@SP\nA=M\nM=0\n@SP\nM=M+1\n"*int(nVars))

    def writeReturn(self):
        # endFrame = LCL
        self.write("@LCL\nD=M\n@endFrame\n")
        # returnAddr = *(endFrame - 5)
        self.write("M=D\n@5\nAD=D-A\nD=M\n@returnAddr\nM=D\n")
        # *ARG = pop()
        self.write("@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n")
        # SP = ARG + 1
        self.write("@ARG\nD=M+1\n@SP\nM=D\n")
        # THAT = *(endFrame - 1)
        self.write("@endFrame\nAM=M-1\nD=M\n@THAT\nM=D\n")
        # THIS = *(endFrame - 2)
        self.write("@endFrame\nAM=M-1\nD=M\n@THIS\nM=D\n")
        # ARG = *(endFrame - 3)
        self.write("@endFrame\nAM=M-1\nD=M\n@ARG\nM=D\n")
        # LCL = *(endFrame - 4)
        self.write("@endFrame\nAM=M-1\nD=M\n@LCL\nM=D\n")
        # goto returnAddr
        self.write("@returnAddr\nA=M\n0;JMP\n")

    def writeCall(self, functionName, nArgs):
        # push function.return address
        self.write("@{function_name}$return.{i}\n".format(function_name=functionName, i=self.call_count))
        self.write("D=A\n@SP\nAM=M+1\nA=A-1\nM=D\n")
        # push LCL, ARG, THIS, THAT
        for i in ["LCL", "ARG", "THIS", "THAT"]:
            self.write("@{segment}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n".format(segment=i))
        # ARG = SP - nArgs - 5
        self.write("@SP\nD=M\n@{n_args}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n".format(n_args=nArgs))
        # LCL - SP
        self.write("@SP\nD=M\n@LCL\nM=D\n")
        # goto functionName
        self.write("@{function_name}\n0;JMP\n".format(function_name=functionName))
        # label function.return address
        self.write("({function_name}$return.{i})\n".format(function_name=functionName, i=self.call_count))
        self.call_count += 1    # increment call count

    def writeInit(self):
        # Initialize stack
        self.write("@256\nD=A\n@SP\nM=D\n")
        # call Sys.init 0
        self.writeCall("Sys.init", "0")

    def writeComment(self, line):
        """Write VM commands as comment into file."""
        self.write("  //" + line + "\n")

    def close(self):
        self.outfile.close()    # close file

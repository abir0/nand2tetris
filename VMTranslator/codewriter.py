

class CodeWriter:

    segment_name = {
        "local" : "LCL",
        "argument" : "ARG",
        "this" : "THIS",
        "that" : "THAT"
    }

    arithmatic_map = {
                "add" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n",
                "sub" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n",
                "neg" : "@SP\nA=M-1\nM=-M\n",
                "and" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n",
                "or" : "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n",
                "not" : "@SP\nA=M-1\nM=!M\n",
                "eq" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_EQ\nD;JNE\n@SP\nA=M-1\nM=-1\n(END_EQ)\n",
                "gt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_GT\nD;JLE\n@SP\nA=M-1\nM=-1\n(END_GT)\n",
                "lt" : "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\nM=0\n@END_LT\nD;JGE\n@SP\nA=M-1\nM=-1\n(END_LT)\n"
    }

    pushpop_map = {
            "push segment" : "@{i}\nD=A\n@{segment}\nA=M+D\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop segment" : "@{i}\nD=A\n@{segment}\nAD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "push temp" : "@{i}\nD=A\n@5\nA=A+D\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop temp" : "@{i}\nD=A\n@5\nAD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "push constant" : "@{i}\nD=A\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "push pointer" : "@{thisthat}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop pointer" : "@SP\nAM=M-1\nD=M\n@{thisthat}\nM=D\n",
            "push static" : "@{filename}.{i}\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop static" : "@SP\nAM=M-1\nD=M\n@{filename}.{i}\nM=D\n"
    }

    def __init__(self, filename):
        self.filename = filename.replace(".vm", "").replace("./", "").replace(".\\", "")
        self.outfile = open(self.filename + ".asm", "w")
        self.outfile.write("// Translation of {} file\n".format(self.filename + ".asm"))

    def writeArithmatic(self, command):
        self.outfile.write(CodeWriter.arithmatic_map[command])

    def writePushPop(self, command, segment, index):
        if segment in CodeWriter.segment_name:
            code = CodeWriter.pushpop_map[command + " " + "segment"]
            code = code.format(i = str(index), segment = CodeWriter.segment_name[segment])
            self.outfile.write(code)

        elif segment == "temp":
            code = CodeWriter.pushpop_map[command + " " + segment]
            code = code.format(i = str(index))
            self.outfile.write(code)

        elif segment == "constant":
            code = CodeWriter.pushpop_map[command + " " + segment]
            code = code.format(i = str(index))
            self.outfile.write(code)

        elif segment == "pointer":
            if index == 0:
                code = CodeWriter.pushpop_map[command + " " + segment]
                code = code.format(thisthat = "THIS")
                self.outfile.write(code)
            elif index == 1:
                code = CodeWriter.pushpop_map[command + " " + segment]
                code = code.format(thisthat = "THAT")
                self.outfile.write(code)

        elif segment == "static":

            code = CodeWriter.pushpop_map[command + " " + segment]
            code = code.format(filename = self.filename, i = str(index))
            self.outfile.write(code)

    def writeComment(self, line):
        self.outfile.write("//" + line + "\n")

    def close(self):
        print("Done")
        self.outfile.close()


#if __name__ == "__main__":

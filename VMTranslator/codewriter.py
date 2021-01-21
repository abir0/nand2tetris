

class CodeWriter:

    segment_name = {
        "local" : "LCL",
        "argument" : "ARG",
        "this" : "THIS",
        "that" : "THAT",
        "temp" : "TEMP"

    }

    arithmatic_map = {
                "add" : "@SP\nAM=M-1\nD=M\nA=M-1\nM=M+D\n",
                "sub" : "@SP\nAM=M-1\nD=M\nA=M-1\nM=M-D\n",
                "neg" : "@SP\nA=M-1\nM=-M\n",
                "and" : "@SP\nAM=M-1\nD=M\nA=M-1\nM=M&D\n",
                "or" : "@SP\nAM=M-1\nD=M\nA=M-1\nM=M|D\n",
                "not" : "@SP\nA=M-1\nM=!M\n",
                "eq" : "@SP\nAM=M-1\nD=M\nA=M-1\nD=M-D\nM=0\n@END_EQ\nD;JNE\n@SP\nA=M-1\nM=-1\n(END_EQ)\n",
                "gt" : "@SP\nAM=M-1\nD=M\nA=M-1\nD=M-D\nM=0\n@END_GT\nD;JLE\n@SP\nA=M-1\nM=-1\n(END_GT)\n",
                "lt" : "@SP\nAM=M-1\nD=M\nA=M-1\nD=M-D\nM=0\n@END_LT\nD;JGE\n@SP\nA=M-1\nM=-1\n(END_LT)\n"
    }

    pushpop_map = {
            "push segment" : "@i\nD=M\n@segment\nA=D+M\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop segment" : "@i\nD=M\n@segment\nA=D+M\nD=A\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D\n",
            "push constant" : "@i\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "push pointer" : "@thisthat\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop pointer" : "@SP\nAM=M-1\nD=M\n@thisthat\nM=D\n",
            "push static" : "@filename.i\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop static" : "@SP\nAM=M-1\nD=M\n@filename.i\nM=D\n"
    }

    def __init__(self, filename):
        self.filename = filename.replace(".vm", ".asm")
        self.outfile = open(filename, "w")
        self.outfile.write("\n")

    def writeArithmatic(self, command):
        self.outfile.write(CodeWriter.arithmatic_map[command])

    def writePushPop(self, command, segment, index):
        if segment in CodeWriter.segment_name:
            code = CodeWriter.pushpop_map[command + " " + "segment"]
            code.replace("i", str(index))
            code.replace("segment", CodeWriter.segment_name[segment])
            self.outfile.write(code)
        elif segment == "constant":
            code = CodeWriter.pushpop_map[command + " " + segment]
            code.replace("i", str(index))
            self.outfile.write(code)
        elif segment == "pointer":
            if index == 0:
                code = CodeWriter.pushpop_map[command + " " + segment]
                code.replace("thisthat", "THIS")
                self.outfile.write(code)
            elif index == 1:
                code = CodeWriter.pushpop_map[command + " " + segment]
                code.replace("thisthat", "THAT")
                self.outfile.write(code)
        elif segment == "static":
            code = CodeWriter.pushpop_map[command + " " + segment]
            code.replace("filename.i", self.filename + "." + str(index))
            self.outfile.write(code)

    @staticmethod
    def writeComment(line):
        return "// " + line

    def close(self):
        print("Done")
        self.outfile.close()


#if __name__ == "__main__":

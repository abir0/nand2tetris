

class CodeWriter:

    segment_map = {
            "SP"    : 0,
            "LCL"   : 1,
            "ARG"   : 2,
            "THIS"  : 3,
            "THAT"  : 4,
            "R13"   : 13,
            "R14"   : 14,
            "R15"   : 15
    }

    base_addr = {
            "temp"  : 5,
            "static": 16,
            "stack" : 256
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
            "push local" = "@i\nD=M\n@segment\nA=D+M\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop local" = "@i\nD=M\n@segment\nA=D+M\nD=A\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D\n",
            "push constant" = "@i\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "push pointer" = "@thisthat\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop pointer" = "@SP\nAM=M-1\nD=M\n@thisthat\nM=D\n",
            "push static" = "@filename.i\nD=M\n@SP\nAM=M+1\nA=A-1\nM=D\n",
            "pop static" = "@SP\nAM=M-1\nD=M\n@filename.i\nM=D\n"
    }

    def __init__(self, filename):
        with open(filename.replace(".vm", ".asm"), "w") as outfile:
            outfile.write("\n")

    @staticmethod
    def writeArithmatic(self,command):
        return CodeWriter.arithmatic_map[command]

    @staticmethod
    def writePushPop(command, segment, index):
        return CodeWriter.pushpop_map[command]


if __name__ == "__main__":
    a = CodeWriter("Test.vm")
    a.writeArithmatic("add")

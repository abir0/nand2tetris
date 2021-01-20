

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
                "add" : "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M+D\n",
                "sub" : "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M-D\n",
                "neg" : "@SP\nA=M-1\nM=-M\n",
                "and" : "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M&D\n",
                "or" : "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nM=M|D\n",
                "not" : "@SP\nA=M-1\nM=!M\n",
                "eq" : "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\n@GOTO\nD;JEQ\n@SP\nA=M-1\nM=-1\n(GOTO)\n@SP\nA=M-1\nM=1\n",
                "gt" : "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\n@GOTO\nD;JEQ\n@SP\nA=M-1\nM=-1\n(GOTO)\n@SP\nA=M-1\nM=1\n",
                "lt" : "@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\n@GOTO\nD;JEQ\n@SP\nA=M-1\nM=-1\n(GOTO)\n@SP\nA=M-1\nM=1\n"
    }

    pushpop_map = {

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
    a.close()

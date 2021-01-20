

class CodeWriter:

    segment_map = {
            "SP"    : 0,
            "LCL"   : 1,
            "ARG"   : 2,
            "THIS"  : 3,
            "THAT"  : 4,
            "temp"  : 5,
            "R13"   : 13,
            "R14"   : 14,
            "R15"   : 15,
            "static": 16,
            "stack" : 256,
            }

    def __init__(self, filename):
        outfile = open(filename.replace(".vm", ".asm"), "w")

    @staticmethod
    def writeArithmatic(self, command):
        return

    @staticmethod
    def writePushPop(self, command, segment, index):
        return

    def close(self):
        outfile.close()

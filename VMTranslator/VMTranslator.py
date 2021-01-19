import sys
import re


class Parser:

    def __init__(self, filename):
        with open(filename, "r") as infile:
            self.commands = list(filter(len, [re.sub(r"//.*$", "", line).strip() for line in lines]))

    def hasMoreCommads(self):
        return self.commands > 0

    def nextCommad(self):
        self.command = self.commands.pop(0)

    def isValidCommand(self):
        return len(self.command.split(" ")) == 1 or len(self.command.split(" ")) == 3

    def commandType(self):
        if self.command.split(" ")[0].lower() is "push":
            return "C_PUSH"
        elif self.command.split(" ")[0].lower() is "pop":
            return "C_POP"
        else:
            return "C_ARITHMATIC"

    def firstArgument(self):
        if len(self.command.split(" ")) == 1:
            return self.command.split(" ")[0]
        else:
            return self.command.split(" ")[1]

    def secondArgument(self):
        return int(self.command.split(" ")[2])


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

    def writeArithmatic(self, command):
        return

    def writePushPop(self, command, segment, index):
        return

    def close(self):
        outfile.close()


def main():
    return


if __name__ == "__main__":
    main()

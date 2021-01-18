import sys
import re


class Parser:

    def __init__(self, filename):
        with open(filename, "r") as infile:
            self.lines = list(infile)

    def commentOut(self):
        self.lines = filter(len, [re.sub(r"//.*$", "", line).strip() for line in lines])

    def nextLine(self):
        self.line = self.lines.pop(0)

    def isValidLine(self):
        return len(self.line.split(" ")) == 1 or len(self.line.split(" ")) == 3

    def firstWord(self):
        return self.line.split(" ")[0]

    def secondWord(self):
        return self.line.split(" ")[1]

    def thirdWord(self):
        return self.line.split(" ")[2]


class CodeWriter:

    MAPS = ""   # Work in progress

    def __init__(self, filename):
        return

    def Arithmatic(self):
        return

    def PushPop(self):
        return

    def translateCode(self):
        return


def main():
    return


if __name__ == "__main__":
    main()

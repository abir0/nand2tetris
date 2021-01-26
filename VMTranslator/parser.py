import re
import sys


class Parser:
    """Parser class for VM translator."""

    COMMAND_TYPE = {
            "push" : "C_PUSH",
             "pop" : "C_POP",
             "add" : "C_ARITHMATIC",
             "sub" : "C_ARITHMATIC",
             "neg" : "C_ARITHMATIC",
             "and" : "C_ARITHMATIC",
             "or" : "C_ARITHMATIC",
             "not" : "C_ARITHMATIC",
             "eq" : "C_ARITHMATIC",
             "gt" : "C_ARITHMATIC",
             "lt" : "C_ARITHMATIC",
             "label" : "C_LABEL",
             "goto" : "C_GOTO",
             "if-goto" : "C_IFGOTO",
             "function" : "C_FUNCTION",
             "return" : "C_RETURN",
             "call" : "C_CALL"
    }

    def __init__(self, data):
        # Remove empty line using len() function into filter
        self.lines = list(filter(len, data))

    def hasMoreCommads(self):
        """Return True if there are more items in the list."""
        return bool(self.lines)

    def nextCommand(self):
        """Put the first item of the list into current line."""
        self.line = self.lines.pop(0)     # pop() method also removes it from the list

    def sourceLine(self):
        """Return the current line."""
        return self.line.strip()

    def commandType(self):
        """Return the command type of the current line."""
        try:
            return Parser.COMMAND_TYPE[self.line.split()[0]]
        except :
            return "NO_COMMAND"

    def getCommand(self):
        """Return the command of the current line."""
        return self.line.split()[0]

    def firstArgument(self):
        """Return the line's first argument."""
        return self.line.split()[1]

    def secondArgument(self):
        """Return the line's second argument."""
        return self.line.split()[2]


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: .\Parser.py <filename>")
        sys.exit(1)

    with open(sys.argv[1], "r") as infile:
        data = infile.readlines()

    P = Parser(data)

    count = 0
    print("SL | TYPE | COMMAND")
    print("-------------------")
    while P.hasMoreCommads():
        P.nextCommad()
        count += 1
        print("{} | {} | {}".format(count, re.sub("C_", "", P.commandType()), P.sourceLine()))

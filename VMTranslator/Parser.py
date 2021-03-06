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
        self.line = None
        self.line_count = 0

    def hasMoreCommads(self):
        """Return True if there are more items in the list."""
        return bool(self.lines)

    def nextCommand(self):
        """Put the first item of the list into current line."""
        self.line = self.lines.pop(0)     # pop() method also removes it from the list

    def sourceLine(self):
        """Return the current line."""
        return self.line.strip()

    def lineCount(self):
        if not self.commandType() == "NO_COMMAND":
            self.line_count += 1
            return self.line_count

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
        print("Usage: .\parser.py <filename>")
        sys.exit(1)

    with open(sys.argv[1], "r") as infile:
        data = infile.readlines()

    P = Parser(data)

    commands = {}
    while P.hasMoreCommads():
        P.nextCommand()
        commands[P.commandType()] = commands.get(P.commandType(), 0) + 1

    for key, val in sorted(commands.items(), key=lambda x: x[1], reverse=True):
        print("{}: {}".format(key, val))

    print("Total lines: {} ".format(sum(commands.values())))

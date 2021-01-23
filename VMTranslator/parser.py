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

    def __init__(self, filename):
        with open(filename, "r") as infile:
            # Remove comments and filter each line using len() function
            self.commands = list(filter(len, [re.sub(r"//.*$", "", line).strip() for line in infile.readlines()]))

    def hasMoreCommads(self):
        """Return True if there are more items in the list."""
        return bool(self.commands)

    def nextCommad(self):
        """Put the first item of the list into current command."""
        self.command = self.commands.pop(0)     # pop() method also removes it from the list

    def getCommand(self):
        """Return the current command."""
        return self.command

    def commandType(self):
        """Return the command type of the current command."""
        return Parser.COMMAND_TYPE[self.command.split()[0]]

    def commandName(self):
        """Return the command name of the current command."""
        return self.command.split()[0]

    def firstArgument(self):
        """Return the command's first argument of the current command."""
        return self.command.split()[1]

    def secondArgument(self):
        """Return the command's second argument of the current command."""
        return self.command.split()[2]


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: .\Parser.py <filename>")
        sys.exit(1)
        
    P = Parser(sys.argv[1])

    while P.hasMoreCommads():
        P.nextCommad()
        print("Command: {}Type: {}".format(P.getCommand(), re.sub("C_", "", P.commandType())))

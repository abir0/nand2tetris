import re

class Parser:

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
             "lt" : "C_ARITHMATIC"
    }

    def __init__(self, filename):
        with open(filename, "r") as infile:
            self.commands = list(filter(len, [re.sub(r"//.*$", "", line).strip() for line in infile.readlines()]))

    def hasMoreCommads(self):
        return len(self.commands) > 0

    def nextCommad(self):
        self.command = self.commands.pop(0)

    def getCommand(self):
        return self.command

    def commandType(self):
        return Parser.COMMAND_TYPE[self.command.split(" ")[0]]

    def firstArgument(self):
        if len(self.command.split(" ")) == 1:
            return self.command.split(" ")[0]
        else:
            return self.command.split(" ")[1]

    def secondArgument(self):
        return self.command.split(" ")[2]


#if __name__ == "__main__":



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
            self.commands = list(filter(len, [re.sub(r"//.*$", "", line).strip() for line in lines]))

    def hasMoreCommads(self):
        return self.commands > 0

    def nextCommad(self):
        self.command = self.commands.pop(0)

    @staticmethod
    def isValidCommand():
        return len(Parser.command.split(" ")) == 1 or len(Parser.command.split(" ")) == 3

    @staticmethod
    def commandType():
        return Parser.COMMAND_TYPE[Parser.command.split(" ")[0]]

    @staticmethod
    def firstArgument():
        if len(Parser.command.split(" ")) == 1:
            return Parser.command.split(" ")[0]
        else:
            return Parser.command.split(" ")[1]

    @staticmethod
    def secondArgument():
        return int(Parser.command.split(" ")[2])


if __name__ == "__main__":
    # Work in progress

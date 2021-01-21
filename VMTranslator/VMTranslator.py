import sys
import re
from CodeWriter import *
from Parser import *

def main(filename):

    try:
        P = Parser(filename)

    except FileNotFoundError:
        print("No such file: \'{}\'\nPlease enter correct filename".format(filename))
        sys.exit(1)

    while P.hasMoreCommads():
        P.nextCommad()
        if not P.isValidCommand():
            print("Command is not valid.")
            sys.exit(1)

        C = CodeWriter(filename)
        if P.commandType() == "C_ARITHMATIC":
            C.writeComment(P.command)
            C.writeArithmatic(P.firstArgument())
        elif P.commandType() == "C_PUSH":
            C.writeComment(P.command)
            C.writePushPop("push", P.firstArgument(), P.secondArgument())
        elif P.commandType() == "C_POP":
            C.writeComment(P.command)
            C.writePushPop("pop", P.firstArgument(), P.secondArgument())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: VMTranslator <filename>")
        sys.exit(1)

    main(sys.argv[1])

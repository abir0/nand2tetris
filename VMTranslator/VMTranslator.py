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

    C = CodeWriter(filename)

    while P.hasMoreCommads():

        P.nextCommad()

        if P.commandType() == "C_ARITHMATIC":
            C.writeComment(P.getCommand())
            C.writeArithmatic(P.firstArgument())

        elif P.commandType() == "C_PUSH":
            C.writeComment(P.getCommand())
            C.writePushPop("push", P.firstArgument(), P.secondArgument())

        elif P.commandType() == "C_POP":
            C.writeComment(P.getCommand())
            C.writePushPop("pop", P.firstArgument(), P.secondArgument())

    C.close()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: VMTranslator <filename>")
        sys.exit(1)

    main(sys.argv[1])

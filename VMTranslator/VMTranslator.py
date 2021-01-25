import sys
import os
import re
from Parser import Parser
from CodeWriter import CodeWriter


def main(filename):

    try:
        with open(filename, "r") as infile:
            data = infile.readlines()
    except FileNotFoundError:
        print("No such file: \'{}\'\nPlease enter correct filename".format(filename))
        sys.exit(1)

    P = Parser(data)
    C = CodeWriter(filename)    # open the file into CodeWriter

    while P.hasMoreCommads():

        P.nextCommad()  # put next line into current command

        if P.commandType() == "C_ARITHMATIC":   # write arithmatic commands
            C.writeComment(P.getCommand())
            C.writeArithmatic(P.commandName())

        elif P.commandType() == "C_PUSH":   # write push commands
            C.writeComment(P.getCommand())
            C.writePushPop(P.commandName(), P.firstArgument(), P.secondArgument())

        elif P.commandType() == "C_POP":    # write pop commands
            C.writeComment(P.getCommand())
            C.writePushPop(P.commandName(), P.firstArgument(), P.secondArgument())

        elif P.commandType() == "C_LABEL":
            pass

        elif P.commandType() == "C_GOTO":
            pass

        elif P.commandType() == "C_IFGOTO":
            pass

        elif P.commandType() == "C_FUNCTION":
            pass

        elif P.commandType() == "C_RETURN":
            pass

        elif P.commandType() == "C_CALL":
            pass

    C.close()   # don't forget to close the file

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: VMtranslator <filename>")
        sys.exit(1)

    main(sys.argv[1])

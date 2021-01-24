import sys
import re
from codewriter import CodeWriter
from parser import Parser

def main(filename):

    try:
        P = Parser(filename)
    except FileNotFoundError:
        print("No such file: \'{}\'\nPlease enter correct filename".format(filename))
        sys.exit(1)

    C = CodeWriter(filename)    # open the file into CodeWriter

    while P.hasMoreCommads():

        P.nextCommad()  # put next line into current command

        if P.commandType() == "C_ARITHMATIC":   # write arithmatic commands
            C.writeComment(P.getCommand())
            C.writeArithmatic(P.commandName())

        elif P.commandType() == "C_PUSH":   # write push commands
            C.writeComment(P.getCommand())
            C.writePushPop("push", P.firstArgument(), P.secondArgument())

        elif P.commandType() == "C_POP":    # write pop commands
            C.writeComment(P.getCommand())
            C.writePushPop("pop", P.firstArgument(), P.secondArgument())

    C.close()   # don't forget to close the file

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: VMTranslator <filename>")
        sys.exit(1)

    main(sys.argv[1])

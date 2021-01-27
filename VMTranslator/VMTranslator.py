import sys
import os
import re
from Parser import Parser
from CodeWriter import CodeWriter


def main(filepath):

    try:
        if os.path.isfile(filepath):
            with open(filepath, "r") as infile:
                data = infile.readlines()
        else:
            data = []
            for filename in os.listdir(filepath):
                if not file.endswith(".vm"):
                    continue
                with open(os.path.join(filepath, filename), "r") as infile:
                    data += infile.readlines()
    except FileNotFoundError:
        print("No such file: \'{}\'\nPlease enter correct filepath".format(filepath))
        sys.exit(1)

    P = Parser(data)
    C = CodeWriter(filepath)    # open the file into CodeWriter

    while P.hasMoreCommads():

        P.nextCommand()  # put next line into current command

        if P.commandType() == "NO_COMMAND":
            C.writeComment(P.sourceLine())

        elif P.commandType() == "C_PUSH":   # write push commands
            C.writeComment(P.sourceLine())
            C.writePushPop(P.getCommand(), P.firstArgument(), P.secondArgument())

        elif P.commandType() == "C_POP":    # write pop commands
            C.writeComment(P.sourceLine())
            C.writePushPop(P.getCommand(), P.firstArgument(), P.secondArgument())

        elif P.commandType() == "C_ARITHMATIC":   # write arithmatic commands
            C.writeComment(P.sourceLine())
            C.writeArithmatic(P.getCommand())

        elif P.commandType() == "C_LABEL":
            C.writeComment(P.sourceLine())
            C.writeLabel(P.firstArgument())

        elif P.commandType() == "C_GOTO":
            C.writeComment(P.sourceLine())
            C.writeGoto(P.firstArgument())

        elif P.commandType() == "C_IFGOTO":
            C.writeComment(P.sourceLine())
            C.writeIfgoto(P.firstArgument())

        elif P.commandType() == "C_FUNCTION":
            C.writeComment(P.sourceLine())

        elif P.commandType() == "C_RETURN":
            C.writeComment(P.sourceLine())

        elif P.commandType() == "C_CALL":
            C.writeComment(P.sourceLine())

    C.close()   # don't forget to close the file

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: VMtranslator <filepath>")
        sys.exit(1)

    main(sys.argv[1])

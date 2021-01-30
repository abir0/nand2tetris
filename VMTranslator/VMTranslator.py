import sys
import os
import re
from Parser import Parser
from CodeWriter import CodeWriter


def main(filepath):

    if not os.path.exists(filepath):
        print("No such file: \'{}\'\nPlease enter correct filepath".format(filepath))
        sys.exit(1)

    if os.path.isfile(filepath):
        bootstrap_flag = False
        with open(filepath, "r") as infile:
            data = infile.readlines()

        writeFile(data, filepath, bootstrap_flag)

    elif os.path.isdir(filepath):
        bootstrap_flag = True
        for filename in os.listdir(filepath):
            if not filename.endswith(".vm"):
                continue
            with open(os.path.join(filepath, filename), "r") as infile:
                data = infile.readlines()

            writeFile(data, filepath, bootstrap_flag)


def writeFile(data, filepath, bootstrap_flag):

    P = Parser(data)
    C = CodeWriter(filepath)    # open the file into CodeWriter

    if bootstrap_flag:
        C.writeComment("call Sys.init 0")
        C.writeBootstrap()

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
            C.writeFunction(P.firstArgument(), P.secondArgument())

        elif P.commandType() == "C_RETURN":
            C.writeComment(P.sourceLine())
            C.writeReturn()

        elif P.commandType() == "C_CALL":
            C.writeComment(P.sourceLine())
            C.writeCall(P.firstArgument(), P.secondArgument())

    C.close()   # don't forget to close the file

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: VMtranslator <filepath>")
        sys.exit(1)

    main(sys.argv[1])

import sys
import os
import re
from Parser import Parser
from CodeWriter import CodeWriter


def main(filepath):

    if not os.path.exists(filepath):
        print("No such file: \'{}\'\nPlease enter correct filepath".format(filepath))
        sys.exit(1)

    filepath = re.sub(r"\\$", "", filepath)
    out_filename = os.path.basename(filepath)
    out_filename = out_filename.replace(".vm", "")

    if os.path.exists(out_filename + ".asm"):
        os.remove(out_filename + ".asm")

    if os.path.isfile(filepath):

        with open(filepath, "r") as infile:
            data = infile.readlines()

        P = Parser(data)
        C = CodeWriter(out_filename)

        writeFile(parser=P, code_writer=C)

    elif os.path.isdir(filepath):

        for filename in os.listdir(filepath):
            if not filename.endswith(".vm"):
                continue
            with open(os.path.join(filepath, filename), "r") as infile:
                data = infile.readlines()

            P = Parser(data)
            C = CodeWriter(out_filename)

            C.writeComment("call Sys.init 0")
            C.writeInit()

            writeFile(parser=P, code_writer=C)


def writeFile(parser, code_writer):

    while parser.hasMoreCommads():

        parser.nextCommand()  # put next line into current command

        if parser.commandType() == "NO_COMMAND":
            code_writer.writeComment(parser.sourceLine())

        elif parser.commandType() == "C_PUSH":   # write push commands
            code_writer.writeComment(parser.sourceLine())
            code_writer.writePushPop(parser.getCommand(), parser.firstArgument(), parser.secondArgument())

        elif parser.commandType() == "C_POP":    # write pop commands
            code_writer.writeComment(parser.sourceLine())
            code_writer.writePushPop(parser.getCommand(), parser.firstArgument(), parser.secondArgument())

        elif parser.commandType() == "C_ARITHMATIC":   # write arithmatic commands
            code_writer.writeComment(parser.sourceLine())
            code_writer.writeArithmatic(parser.getCommand())

        elif parser.commandType() == "C_LABEL":
            code_writer.writeComment(parser.sourceLine())
            code_writer.writeLabel(parser.firstArgument())

        elif parser.commandType() == "C_GOTO":
            code_writer.writeComment(parser.sourceLine())
            code_writer.writeGoto(parser.firstArgument())

        elif parser.commandType() == "C_IFGOTO":
            code_writer.writeComment(parser.sourceLine())
            code_writer.writeIfgoto(parser.firstArgument())

        elif parser.commandType() == "C_FUNCTION":
            code_writer.writeComment(parser.sourceLine())
            code_writer.writeFunction(parser.firstArgument(), parser.secondArgument())

        elif parser.commandType() == "C_RETURN":
            code_writer.writeComment(parser.sourceLine())
            code_writer.writeReturn()

        elif parser.commandType() == "C_CALL":
            code_writer.writeComment(parser.sourceLine())
            code_writer.writeCall(parser.firstArgument(), parser.secondArgument())

    code_writer.close()   # don't forget to close the file

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: VMtranslator <filepath>")
        sys.exit(1)

    main(sys.argv[1])

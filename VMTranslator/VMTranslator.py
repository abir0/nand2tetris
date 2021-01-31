import sys
import os
import re
from Parser import Parser
from CodeWriter import CodeWriter


def main(filepath):

    out_filename, filenames = parseFilePath(filepath)

    if os.path.exists(out_filename):
        os.remove(out_filename)

    if os.path.isfile(filepath):
        with open(filepath, "r") as infile:
            data = infile.readlines()

        parser = Parser(data)
        code_writer = CodeWriter(out_filename, filenames[0])

        writeFile(parser, code_writer)

    elif os.path.isdir(filepath):
        for filename in filenames:
            full_path = os.path.join(filepath, filename + ".vm")
            with open(full_path, "r") as infile:
                data = infile.readlines()

            parser = Parser(data)
            code_writer = CodeWriter(out_filename, filename)

            if filenames[0] == filename:
                code_writer.writeComment("call Sys.init 0")
                code_writer.writeInit()
            writeFile(parser, code_writer)

def parseFilePath(path):

    clean_path = path.replace(".vm", "")
    clean_path = re.sub(r"\\$", "", clean_path)

    output_filename = clean_path + ".asm"

    try:
        filenames = [filename.replace(".vm","") for filename in os.listdir(path) if filename.endswith(".vm")]
    except NotADirectoryError:
        filenames = [os.path.basename(clean_path)]
    except FileNotFoundError:
        print("No such file: \'{}\'\nPlease enter correct filepath".format(path))
        sys.exit(1)

    return output_filename, filenames


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

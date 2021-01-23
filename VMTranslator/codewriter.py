

class CodeWriter:

    SEGMENT_NAME = {
        "local" : "LCL",
        "argument" : "ARG",
        "this" : "THIS",
        "that" : "THAT"
    }

    ARITHMATIC_MAP = {
                "add" : ("@SP\n" +
                         "AM=M-1\n" +
                         "D=M\n" +
                         "A=A-1\n" +
                         "M=M+D\n"),
                "sub" : ("@SP\n" +
                         "AM=M-1\n" +
                         "D=M\n" +
                         "A=A-1\n" +
                         "M=M-D\n"),
                "neg" : ("@SP\n" +
                         "A=M-1\n" +
                         "M=-M\n"),
                "and" : ("@SP\n" +
                         "AM=M-1\n"
                         "D=M\n" +
                         "A=A-1\n" +
                         "M=M&D\n"),
                "or" : ("@SP\n" +
                        "AM=M-1\n" +
                        "D=M\n" +
                        "A=A-1\n" +
                        "M=M|D\n"),
                "not" : ("@SP\n" +
                         "A=M-1\n" +
                         "M=!M\n"),
                "eq" : ("@SP\n" +
                        "AM=M-1\n" +
                        "D=M\n" +
                        "A=A-1\n" +
                        "D=M-D\n" +
                        "M=0\n" +
                        "@END_EQ_{i}\n" +
                        "D;JNE\n" +
                        "@SP\n" +
                        "A=M-1\n" +
                        "M=-1\n" +
                        "(END_EQ_{i})\n"),
                "gt" : ("@SP\n" +
                        "AM=M-1\n" +
                        "D=M\n" +
                        "A=A-1\n" +
                        "D=M-D\n" +
                        "M=0\n" +
                        "@END_GT_{i}\n" +
                        "D;JLE\n" +
                        "@SP\n" +
                        "A=M-1\n" +
                        "M=-1\n" +
                        "(END_GT_{i})\n"),
                "lt" : ("@SP\n" +
                        "AM=M-1\n" +
                        "D=M\n" +
                        "A=A-1\n" +
                        "D=M-D\n" +
                        "M=0\n" +
                        "@END_LT_{i}\n" +
                        "D;JGE\n" +
                        "@SP\n" +
                        "A=M-1\n" +
                        "M=-1\n" +
                        "(END_LT_{i})\n")
    }

    PUSHPOP_MAP = {
            "push segment" : ("@{i}\n" +
                              "D=A\n" +
                              "@{segment}\n" +
                              "A=M+D\n" +
                              "D=M\n" +
                              "@SP\n" +
                              "AM=M+1\n" +
                              "A=A-1\n" +
                              "M=D\n"),
            "pop segment" : ("@{i}\n" +
                             "D=A\n" +
                             "@{segment}\n" +
                             "AD=M+D\n" +
                             "@R13\n" +
                             "M=D\n" +
                             "@SP\n" +
                             "AM=M-1\n" +
                             "D=M\n" +
                             "@R13\n" +
                             "A=M\n" +
                             "M=D\n"),
            "push temp" : ("@{i}\n" +
                           "D=A\n" +
                           "@5\n" +
                           "A=A+D\n" +
                           "D=M\n" +
                           "@SP\n" +
                           "AM=M+1\n" +
                           "A=A-1\n" +
                           "M=D\n"),
            "pop temp" : ("@{i}\n" +
                          "D=A\n" +
                          "@5\n" +
                          "AD=A+D\n" +
                          "@R13\n" +
                          "M=D\n" +
                          "@SP\n" +
                          "AM=M-1\n" +
                          "D=M\n" +
                          "@R13\n" +
                          "A=M\n" +
                          "M=D\n"),
            "push constant" : ("@{i}\n" +
                               "D=A\n" +
                               "@SP\n" +
                               "AM=M+1\n" +
                               "A=A-1\n" +
                               "M=D\n"),
            "push pointer" : ("@{pointer}\n" +
                              "D=M\n" +
                              "@SP\n" +
                              "AM=M+1\n" +
                              "A=A-1\n" +
                              "M=D\n"),
            "pop pointer" : ("@SP\n" +
                             "AM=M-1\n" +
                             "D=M\n" +
                             "@{pointer}\n" +
                             "M=D\n"),
            "push static" : ("@{filename}.{i}\n" +
                             "D=M\n" +
                             "@SP\n" +
                             "AM=M+1\n" +
                             "A=A-1\n" +
                             "M=D\n"),
            "pop static" : ("@SP\n" +
                            "AM=M-1\n" +
                            "D=M\n" +
                            "@{filename}.{i}\n" +
                            "M=D\n")
    }

    def __init__(self, filename):
        self.filename = filename.replace(".vm", "").replace("./", "").replace(".\\", "")
        self.outfile = open(self.filename + ".asm", "w")
        self.outfile.write("// Translation of {} file\n".format(self.filename + ".asm"))
        self.jump_count = 0

    def increase_count(self):
        self.jump_count += 1

    def writeArithmatic(self, command):
        if command in ["eq", "gt", "lt"]:
            code = CodeWriter.ARITHMATIC_MAP[command]
            code = code.format(i = self.jump_count)
            self.outfile.write(code)
            CodeWriter.increase_count(self)
        else:
            code = CodeWriter.ARITHMATIC_MAP[command]
            self.outfile.write(code)

    def writePushPop(self, command, segment, index):
        if segment in CodeWriter.SEGMENT_NAME:
            code = CodeWriter.PUSHPOP_MAP[command + " " + "segment"]
            code = code.format(i = str(index), segment = CodeWriter.SEGMENT_NAME[segment])
            self.outfile.write(code)

        elif segment == "temp":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i = str(index))
            self.outfile.write(code)

        elif segment == "constant":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(i = str(index))
            self.outfile.write(code)

        elif segment == "pointer":
            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(pointer = str(3 + int(index)))
            self.outfile.write(code)

        elif segment == "static":

            code = CodeWriter.PUSHPOP_MAP[command + " " + segment]
            code = code.format(filename = self.filename, i = str(index))
            self.outfile.write(code)

    def writeComment(self, line):
        self.outfile.write("//" + line + "\n")

    def close(self):
        self.outfile.close()


#if __name__ == "__main__":

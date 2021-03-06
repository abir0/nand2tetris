

class VMWriter:

    def __init__(self, filename):
        self.out_file = open(filename.replace('.jack', '.vm'), 'w')

    def writePop(self, segment, index):
        self.out_file.write(" ".join(["pop", segment, index]))
        self.out_file.write("\n")

    def writePush(self, segment, index):
        self.out_file.write(" ".join(["push", segment, index]))
        self.out_file.write("\n")

    def writeArithmatic(self, command):
        self.out_file.write(command)
        self.out_file.write("\n")

    def writeLabel(self, label):
        self.out_file.write(" ".join(["label", label]))
        self.out_file.write("\n")

    def writeGoto(self, label):
        self.out_file.write(" ".join(["goto", label]))
        self.out_file.write("\n")

    def writeIf(self, label):
        self.out_file.write(" ".join(["if-goto", label]))
        self.out_file.write("\n")

    def writeCall(self, name, nArgs):
        self.out_file.write(" ".join(["call", name, nArgs]))
        self.out_file.write("\n")

    def writeFunction(self, name, nLocals):
        self.out_file.write(" ".join(["function", name, nLocals]))
        self.out_file.write("\n")

    def writeReturn(self):
        self.out_file.write("return")
        self.out_file.write("\n")

    def close(self):
        self.out_file.close()

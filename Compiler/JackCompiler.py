import sys
from os import listdir
from os.path import exists, isdir, isfile, join
from Tokenizer import Tokenizer
from Parser import CompilationEngine
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class Compiler:

    def __init__(self, path):
        self.filenames = self.get_filenames(path)

    def compileFiles(self):
        for filename in self.filenames:
            E = CompilationEngine(filename)
            E.compileClass()

    @staticmethod
    def get_filenames(path):
        """Return a list of filenames from filepath."""
        filenames = []
        if not exists(path):
            raise FileNotFoundError
        elif isfile(path):
            filenames.append(path)
        elif isdir(path):
            filenames = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and join(path, f).endswith(".jack")]
        return filenames

if __name__ == "__main__":
    C = Compiler(sys.argv[1])
    C.compileFiles()
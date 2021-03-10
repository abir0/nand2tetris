import sys
from os import listdir
from os.path import exists, isdir, isfile, join
from Tokenizer import Tokenizer
from CompilationEngine import CompilationEngine
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class Compiler:

    def __init__(self, path):
        self.filenames = self.get_filenames(path)

    def compileFiles(self):
        verbose = self.parse_arg()
        for filename in self.filenames:
            V = VMWriter(filename, verbose=verbose)
            T = Tokenizer(filename, verbose=verbose)
            T.tokenize()
            E = CompilationEngine(filename, tokens=T, vm_writer=V, verbose=verbose)
            S = SymbolTable()
            E.compileClass(symbol_table=S)
            V.close()
            #print(S.class_table)
            #print(S.subroutine_table)

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

    @staticmethod
    def parse_arg():
        """Parse the CLI argument."""
        try:
            verbose = sys.argv[2]
            if verbose == "--verbose" or verbose == "-v":
                verbose = True
            else:
                verbose = False
        except:
            verbose = False
        return verbose

if __name__ == "__main__":
    C = Compiler(sys.argv[1])
    C.compileFiles()

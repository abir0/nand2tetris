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
        """Compile each file in the given directory using all modules and generate code."""
        verbose = self.parse_arg(sys.argv)

        for filename in self.filenames:
            vm_writer = VMWriter(filename)
            tokenizer = Tokenizer(filename)
            symbol_table = SymbolTable()
            tokenizer.tokenize()
            engine = CompilationEngine(tokens=tokenizer,
                                       vm_writer=vm_writer,
                                       symbol_table=symbol_table,
                                       verbose=verbose)
            engine.compileClass()
            vm_writer.close()

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
    def parse_arg(args):
        """Parse the CLI argument."""
        try:
            verbose = False
            if "--verbose" in args or "-v" in args:
                verbose = True
        except:
            verbose = False
        return verbose

if __name__ == "__main__":
    compiler = Compiler(sys.argv[1])
    compiler.compileFiles()

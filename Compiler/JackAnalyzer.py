import sys
from os import listdir
from os.path import exists, isdir, isfile, join
from Parser import CompilationEngine


def main(path):
    filenames = get_filenames(path)

    for filename in filenames:
        C = CompilationEngine(filename)
        C.compileClass()

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
    main(sys.argv[1])

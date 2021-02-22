import sys
from os import walk
from os.path import exists, isdir, isfile, join


def main(path):
    filenames = get_filenames(path)

    for filename in filenames:
        T = Tokenizer(filename)
        tokens = T.tokenize()
        P = CompilationEngine(tokens)
        while P.hasMoreTokens():
            P.advance()

        T.write_files()


def get_filenames(path):
    """Return a list of filenames from filepath."""
    filenames = []
    if not exists(path):
        raise FileNotFoundError
    elif isfile(path):
        filenames.append(path)
    elif isdir(path):
        filenames = [join(filepath, basename)
                     for filepath, _, basename in walk(path)]
    return filenames


def write_files(filenames, data):
    """Write into the into each files."""
    for i, filename in enumerate(filenames):
        out_filename = filename.replace(".jack", ".xml")
        with open(out_filename, "w") as outfile:
            outfile.write("\n".join(data[i]))


if __name__ == "__main__":
    main(sys.argv[1])

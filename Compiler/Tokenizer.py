import sys
from os import walk
from os.path import exists, isdir, isfile, join
import re


class Tokenizer:
    """Jack Tokenizer class."""

    KEYWORDS = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char",
                "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
    SYMBOLS = {"{", "}", "(", ")", "[", "]", ".", ",", ";",
               "+", "-", "*", "/", "~", "&", "|", "<", ">", "="}

    def __init__(self, filepath):
        self.filenames = Tokenizer.get_filenames(filepath)

    @staticmethod
    def get_filenames(filepath):
        """Return a list of filenames from filepath."""
        filenames = []
        if not exists(filepath):
            raise FileNotFoundError
        elif isfile(filepath):
            filenames.append(filepath)
        elif isdir(filepath):
            filenames = [join(path, file) for path, _, file in walk(filepath)]
        return filenames

    def read_files(self):
        """Read each file and get the data."""
        self.files = {}
        for filename in self.filenames:
            with open(filename, "r") as infile:
                file_data = str(infile.read())
                self.files[filename] = Tokenizer.process_lines(file_data)

    @staticmethod
    def process_lines(file_data):
        """Return the list of words from the file data."""
        comment_pattern1 = r"\/\/.*"
        comment_pattern2 = r"\/\*.*?\*\/"
        file_data = re.sub(comment_pattern1, "", file_data)
        file_data = re.sub(comment_pattern2, "", file_data)
        return file_data.split()

    def tokenize(self):
        """Generate tokens from the data."""
        decimal_pattern = r"[0-9]{1,5}"
        string_pattern = r"\".*?\""
        identifier_pattern = r"[a-zA-Z_][a-zA-Z0-9_]*"

        for file in self.files:
            for word in file:
                pass

    def write_files(self):
        """Write the tokens into each files."""
        for filename in self.filenames:
            out_filename = filename.replace(".jack", ".txt")
            with open(out_filename, "w") as outfile:
                outfile.write("\n".join(self.files[filename]))


if __name__ == "__main__":

    T = Tokenizer(sys.argv[1])
    T.read_files()
    T.write_files()

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

    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        """Read each file and get the data."""

        with open(self.filename, "r") as infile:
            file_data = str(infile.read())
            self.file = Tokenizer.process_lines(file_data)

    @ staticmethod
    def process_lines(file_data):
        """Return the list of words from the file data."""

        comment_pattern1 = r"\/\/.*?(\r\n|\r|\n)"
        comment_pattern2 = r"\/\*.*?\*\/"
        file_data = re.sub(comment_pattern1, "", file_data)
        file_data = re.sub(comment_pattern2, "", file_data)
        return file_data

    def tokenize(self):
        """Generate tokens from the data."""

        tokens = []
        token = ""
        str_flag = False
        for c in str(self.file):
            if c in Tokenizer.SYMBOLS:
                tokens.append(token.strip())
                tokens.append(c)
                token = ""
            elif c in ["\""]:
                str_flag = not str_flag
                tokens.append(token)
                token = ""
            elif c in [" "]:
                if str_flag:
                    token += c
                    continue
                tokens.append(token.strip())
                token = ""
            else:
                token += c
        self.tokens = list(filter(len, tokens))
        return self.tokens

    def write_file(self):
        """Write the tokens into each files."""

        out_filename = self.filename.replace(".jack", ".txt")
        with open(out_filename, "w") as outfile:
            outfile.write("\n".join(self.tokens))


if __name__ == "__main__":

    T = Tokenizer(sys.argv[1])
    T.read_file()
    T.tokenize()
    T.write_file()

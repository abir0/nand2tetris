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

    @staticmethod
    def read_file(filename):
        """Read the file and get its contents."""

        with open(filename, "r") as infile:
            file_data = str(infile.read())

        return file_data

    @staticmethod
    def remove_comments(file_data):
        """Return the list of words from the data."""

        comment_pattern1 = r"\/\/.*?(\r\n|\r|\n)"
        comment_pattern2 = r"\/\*.*?\*\/"

        file_data = re.sub(comment_pattern1, "", file_data)
        file_data = re.sub(comment_pattern2, "", file_data)

        return file_data

    @staticmethod
    def get_tokens(file_data):
        """Return the tokens from the data."""

        tokens = []
        token = ""
        str_flag = False
        for c in str(file_data):
            if c in Tokenizer.SYMBOLS:
                tokens.append(token.strip())
                tokens.append(c)
                token = ""
            elif c in ["\""]:
                str_flag = not str_flag
                tokens.append(c + tokenc + c)
                token = ""
            elif c in [" "]:
                if str_flag:
                    token += c
                    continue
                tokens.append(token.strip())
                token = ""
            else:
                token += c
        tokens = list(filter(len, tokens))
        return tokens

    def tokenize(self):
        """Generate xml labels from the tokens."""

        integer_pattern = r"\b[0-9]{1,5}\b"
        string_pattern = r"\".*?\""
        identifier_pattern = r"\b[A-Za-z_][A-Za-z0-9_]*\b"

        file_data = Tokenizer.read_file(self.filename)
        file_data = Tokenizer.remove_comments(file_data)
        tokens = Tokenizer.get_tokens(file_data)

        for i, token in enumerate(tokens):
            if token in Tokenizer.KEYWORDS:
                tokens[i] = "<keyword> " + token + " </keyword>"
            elif token in Tokenizer.SYMBOLS:
                tokens[i] = "<symbol> " + token + " </symbol>"
            elif re.search(identifier_pattern, token) is not None:
                tokens[i] = "<identifier> " + token + " </identifier>"
            elif re.search(integer_pattern, token) is not None:
                tokens[i] = "<integerConstant> " + \
                    token + " </integerConstant>"
            elif re.search(string_pattern, token) is not None:
                tokens[i] = "<stringConstant> " + token + " </stringConstant>"

        return tokens

    def write(self, tokens):
        """Write the tokens into each files."""

        out_filename = self.filename.replace(".jack", ".xml")
        with open(out_filename, "w") as outfile:
            outfile.write("<tokens>\n")
            outfile.write("\n".join(tokens))
            outfile.write("\n</tokens>")


if __name__ == "__main__":

    T = Tokenizer(sys.argv[1])
    tokens = T.tokenize()
    T.write(tokens)

import sys
from os import walk
from os.path import exists, isdir, isfile, join
import re


class Tokenizer:
    """Jack Tokenizer class."""

    KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char",
                "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
    SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
               "+", "-", "*", "/", "~", "&", "|", "<", ">", "="]

    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.tokens = list()
        self.token = str()
        self.verbose = verbose

    @staticmethod
    def read_file(filename):
        """Read the file and get its contents."""

        with open(filename, "r") as infile:
            file_data = str(infile.read())

        return file_data

    @staticmethod
    def remove_comments(file_data):
        """Remove the comments from the data."""

        comment_pattern1 = r"\/\/.*?(\r\n|\r|\n)"
        comment_pattern2 = r"\/\*[\s\S]*?\*\/"

        file_data = re.sub(comment_pattern1, "", file_data)
        file_data = re.sub(comment_pattern2, "", file_data)

        return file_data

    def tokenize(self):
        """Return the tokens from the data."""

        file_data = Tokenizer.read_file(self.filename)
        file_data = Tokenizer.remove_comments(file_data)

        token = ""
        str_flag = False
        for char in str(file_data):
            if char in Tokenizer.SYMBOLS:
                self.tokens.append(token.strip())
                self.tokens.append(char)
                token = ""
            elif char == "\"":
                str_flag = not str_flag
                if token == "":
                    continue
                self.tokens.append("\"" + token + "\"")
                token = ""
            elif char == " ":
                if str_flag:
                    token += char
                    continue
                self.tokens.append(token.strip())
                token = ""
            else:
                token += char
        self.tokens = list(filter(len, self.tokens))
        if self.verbose:
            print("Tokens:")
            print("`", end="")
            print("`\t`".join(self.tokens), end="")
            print("`", end="")
            print("\n")

    def hasMoreTokens(self):
        """Return whether there are more tokens or not."""
        return bool(self.tokens)

    def advance(self):
        """Take one token from the tokens."""
        if not self.hasMoreTokens():
            print("JackAnalyzer has finished")
            return
        self.token = self.tokens.pop(0)

    def getToken(self):
        return self.token

    def tokenType(self):
        """Return the token type in string."""

        integer_pattern = r"[0-9]{1,5}"
        string_pattern = r"\".*?\""
        identifier_pattern = r"[A-Za-z_][A-Za-z0-9_]*"

        if self.token in Tokenizer.KEYWORDS:
            return "KEYWORD"
        elif self.token in Tokenizer.SYMBOLS:
            return "SYMBOL"
        elif re.search(string_pattern, self.token) is not None:
            return "STR_CONST"
        elif re.search(identifier_pattern, self.token) is not None:
            return "IDENTIFIER"
        elif re.search(integer_pattern, self.token) is not None:
            return "INT_CONST"

    def keyWord(self):
        if self.tokenType() == "KEYWORD":
            return self.token.upper()

    def symbol(self):
        if self.tokenType() == "SYMBOL":
            return self.token

    def identifier(self):
        if self.tokenType() == "IDENTIFIER":
            return str(self.token)

    def intVal(self):
        if self.tokenType() == "INT_CONST":
            return int(self.token)

    def stringVal(self):
        if self.tokenType() == "STR_CONST":
            return str(self.token[1:-1])

    def writeTokens(self):
        """Write the tokens in xml."""

        char_entity = {"{": "&lcub;", "}": "&rcub;", "(": "&lpar;", ")": "&rpar;",
                       "[": "&lsqb", "]": "&rsqb;", ".": "&period;", ",": "&comma;", ";": "&semi;",
                       "+": "&plus;", "-": "&minus;", "*": "&ast;", "/": "&sol;", "~": "&sim;",
                       "&": "&amp;", "|": "&vert;", "<": "&lt;", ">": "&gt;", "=": "&equals;"}

        out_filename = self.filename.replace(".jack", ".xml")
        with open(out_filename, "w") as outfile:
            outfile.write("<tokens>\n")
            while self.hasMoreTokens():
                self.advance()
                if self.tokenType() == "KEYWORD":
                    if self.verbose:
                        print(self.tokenType().ljust(10), "|", self.keyWord())
                    outfile.write("<keyword> " + self.token + " </keyword>\n")

                elif self.tokenType() == "SYMBOL":
                    if self.verbose:
                        print(self.tokenType().ljust(10), "|", self.symbol())
                    outfile.write("<symbol> " + self.token + " </symbol>\n")

                elif self.tokenType() == "IDENTIFIER":
                    if self.verbose:
                        print(self.tokenType().ljust(10), "|", self.identifier())
                    outfile.write("<identifier> " + self.token + " </identifier>\n")

                elif self.tokenType() == "INT_CONST":
                    if self.verbose:
                        print(self.tokenType().ljust(10), "|", self.intVal())
                    outfile.write("<integerConstant> " + self.token + " </integerConstant>\n")

                elif self.tokenType() == "STR_CONST":
                    if self.verbose:
                        print(self.tokenType().ljust(10), "|", self.stringVal())
                    outfile.write("<stringConstant> " + self.token[1:-1] + " </stringConstant>\n")
            outfile.write("</tokens>")


if __name__ == "__main__":

    try:
        verbose = sys.argv[2]
        if verbose == "--verbose" or verbose == "-v":
            verbose = True
    except:
        verbose = False

    T = Tokenizer(sys.argv[1], verbose)
    T.tokenize()
    T.writeTokens(verbose)
    del T

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
        self.tokens = list()
        self.token = str()

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

    def hasMoreTokens(self):
        return bool(self.tokens)

    def advance(self):
        self.token = self.tokens.pop(0)

    def tokenType(self):
        """Generate xml labels from the tokens."""

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

    def writeTokens(self):
        """Write the tokens into each files."""

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
                    outfile.write("<keyword> " + self.token + " </keyword>\n")
                elif self.tokenType() == "SYMBOL":
                    outfile.write(
                        "<symbol> " + self.token + " </symbol>\n")
                elif self.tokenType() == "IDENTIFIER":
                    outfile.write("<identifier> " +
                                  self.token + " </identifier>\n")
                elif self.tokenType() == "INT_CONST":
                    outfile.write("<integerConstant> " +
                                  self.token + " </integerConstant>\n")
                elif self.tokenType() == "STR_CONST":
                    outfile.write("<stringConstant> " +
                                  self.token[1:-1] + " </stringConstant>\n")
            outfile.write("</tokens>")


if __name__ == "__main__":

    T = Tokenizer(sys.argv[1])
    T.tokenize()
    T.writeTokens()

import sys
from pathlib import Path
import re


class Tokenizer:
    """Jack Tokenizer class."""

    # Keywords and symbols in jack language
    KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char",
                "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

    SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
               "+", "-", "*", "/", "~", "&", "|", "<", ">", "="]

    def __init__(self, path):
        self.path = path
        self.tokens = list()
        self.token = str()


    @staticmethod
    def read_file(path):
        """Read the file and get its contents."""
        return Tokenizer.remove_comments(Path(path).expanduser().read_text())


    @staticmethod
    def remove_comments(string):
        """Remove the comments from the data."""

        def remove_block_coments(string):
            return re.sub(r"\/\/.*?(\r\n|\r|\n)", "", string)

        def remove_line_comments(string):
            return re.sub(r"\/\*[\s\S]*?\*\/", "", string)

        def remove_new_lines(string):
            return re.sub(r"(\r\n|\r|\n)", "", string)

        return remove_new_lines(
                    remove_line_comments(
                        remove_block_coments(string)))


    def tokenize(self):
        """Return the tokens from the data."""
        token = ""
        str_flag = False
        for char in self.read_file(self.path):
            if char in self.SYMBOLS:
                if str_flag:
                    token += char
                    continue
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
        if self.token in self.KEYWORDS:
            return "KEYWORD"
        elif self.token in self.SYMBOLS:
            return "SYMBOL"
        elif re.search(r"\".*?\"", self.token) is not None:
            return "STR_CONST"
        elif re.search(r"[A-Za-z_][A-Za-z0-9_]*", self.token) is not None:
            return "IDENTIFIER"
        elif re.search(r"[0-9]{1,5}", self.token) is not None:
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


if __name__ == "__main__":

    T = Tokenizer(sys.argv[1])
    T.tokenize()

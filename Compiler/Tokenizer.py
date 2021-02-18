import sys
from os import walk
from os.path import exists, isdir, isfile, join
import re


class Tokenizer:

    KEYWORDS = {"class", ""}
    SYMBOLS = {"{", ""}

    def __init__(self, filepath):
        self.filenames = Tokenizer.get_filenames(filepath)

    @staticmethod
    def get_filenames(filepath):
        filenames = []
        if not exists(filepath):
            raise FileNotFoundError
        elif isfile(filepath):
            filenames.append(filepath)
        elif isdir(filepath):
            filenames = [join(path, file) for path, _, file in walk(filepath)]
        return filenames

    def read_files(self):
        self.files = {}
        for filename in self.filenames:
            with open(filename, "r") as infile:
                file_data = str(infile.read())
                self.files[filename] = Tokenizer.process_lines(file_data)

    @staticmethod
    def process_lines(file_data):
        comment_pattern1 = r"\/\/.*"
        comment_pattern2 = r"\/\*.*?\*\/"
        file_data = re.sub(comment_pattern1, "", file_data)
        file_data = re.sub(comment_pattern2, "", file_data)
        return file_data.split()

    def tokenize(self):
        pass

    def write_files(self):
        for filename in self.filenames:
            out_filename = filename.replace(".jack", ".txt")
            with open(out_filename, "w") as outfile:
                outfile.write("\n".join(self.files[filename]))


if __name__ == "__main__":

    T = Tokenizer(sys.argv[1])
    T.read_files()
    T.write_files()

import sys
import re

def main(filename):

    open_tag = r'<[^\/]*?>'
    close_tag = r'<\/.*?>'
    with open(filename, 'r') as fh:
        data = fh.readlines()

    with open(filename.replace(".xml", "P.xml"), 'w') as fh:
        indent_level = 0
        for line in data:
            if re.search(close_tag, line) is not None:
                indent_level -= 1
            line = "  " * indent_level + line
            fh.write(line)
            if re.search(open_tag, line) is not None:
                indent_level += 1



if __name__ == "__main__":
    main(sys.argv[1])

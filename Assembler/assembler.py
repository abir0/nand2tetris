import sys
import re
import json


def dec2bin(num):
    """Converts a decimal number to 16-bit binary in string format."""
    bin = ''

    while num != 0:
        quotient = num // 2
        remainder = num % 2
        if remainder == 1:
            bin = '1' + bin
        else:
            bin = '0' + bin
        num = quotient

    # Pad with 0's to match 16 bits
    bin = '0' + (15 - len(bin)) * '0' + bin
    return bin


def map_table(code):
    """Maps the variable names to register addresses."""

    # Dictionary of mappings between pre-defined names
    table = {
        "SP"    : 0,
        "LCL"   : 1,
        "ARG"   : 2,
        "THIS"  : 3,
        "THAT"  : 4,
        "SCREEN": 16384,
        "KBD"   : 24576,
        }

    # R0-R15
    for i in range(0, 16):
        table["R" + str(i)] = i

    # Add user-defined names i.e. variables and gotos
    goto_pattern = r'[^\/]*?\(([A-Za-z0-9$._]+)\)'        # (goto)
    var_pattern = r'[^\/]*?@([A-Za-z$_][A-Za-z0-9$._]*)'  # @variable
    A_pattern = r'[^\/]*?@[0-9]+'                         # @123
    C_pattern = r'[^\/]+?='                               # dest = comp
    C_pattern2 = r'[^\/=]+?;'                             # comp ; jump

    var_list = []   # list of all @-values
    reg = 16        # start after R15
    count = -1      # keep track of instruction memory position

    for line in code:
        goto = re.search(goto_pattern, line)
        var = re.search(var_pattern, line)

        if goto is not None:
            table[goto[1]] = count + 1      # add next position after goto

        elif re.search(A_pattern, line) is not None:
            count += 1

        elif var is not None:
            if var[1] not in var_list:
                var_list.append(var[1])    # append to list if it doesn't exist
            count += 1

        elif re.search(C_pattern, line) is not None:
            count += 1

        elif re.search(C_pattern2, line) is not None:
            count += 1

    for i in var_list:
        try:
            table[i]
        except KeyError:
            table[i] = reg      # if key doesn't exist add it
            reg += 1

    return table


def parser(line):
    """Parses A or C instruction into different components."""
    # Remove comment and whitespace
    line = re.sub(r'//.*', '' , line)   # remove comment
    line = line.strip()                 # remove whitespace

    # Parse A instruction, return int or string
    if line.find('@') == 0:
        try:
            dec = int(line[1:])
            return dec
        except:
            return line[1:]

    else:
        # Parse C instruction, return tuple
        if line.find(';') != -1:
            comp, jump = line.split(';')        # comp ; jump
            dest = "null"

            if comp.find('=') != -1:
                dest, comp = comp.split('=')    # dest = comp ; jump
            return comp, dest, jump

        elif line.find('=') != -1:
            dest, comp = line.split('=')        # dest = comp
            jump = "null"
            return comp, dest, jump

        else:
            return None


def main(args):

    with open(args[0]) as infile:
        data = infile.readlines()

    from instructions import comp, dest, jump

    table = map_table(data)

    machine_code = []

    for line in data:
        parsed = parser(line)

        if type(parsed) is type(()):
            # Join parsed components from corresponding dictionaries
            # and pad with 1's to match 16 bits of A instruction
            bin = '111' + comp[parsed[0]] + dest[parsed[1]] + jump[parsed[2]]

        elif type(parsed) is type(0):
            bin = dec2bin(parsed)

        elif type(parsed) is type(''):
            dec = table[parsed]
            bin = dec2bin(dec)

        else:
            continue

        machine_code.append(bin)

    with open(args[1], "w") as outfile:
        outfile.write('\n'.join(machine_code)) # Join each list item with newline


if __name__ == "__main__":
    main(sys.argv[1:])

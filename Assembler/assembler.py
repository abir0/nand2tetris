import sys
import re


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


def map_table(asm):
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
    variables_list = []   # list of all @-values
    reg = 16        # start after R15
    count = -1      # keep track of instruction memory position

    for line in asm:
        parsed, flag =  parser(line)

        if flag == "GOTO_INSTRUCTION":
            table[parsed] = count + 1      # add next position after goto
        elif flag == "A_DECIMAL":
            count += 1
        elif flag == "A_INSTRUCTION":
            if parsed not in variables_list:
                variables_list.append(parsed)    # append to list if it doesn't exist
            count += 1
        elif flag == "C_INSTRUCTION":
            count += 1

    for i in variables_list:
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
            parsed = int(line[1:])
            flag = "A_DECIMAL"
        except:
            parsed = line[1:]
            flag = "A_INSTRUCTION"

    elif line.startswith("(") and line.endswith(")"):
        parsed = line[1:-1]
        flag = "GOTO_INSTRUCTION"
    else:
        # Parse C instruction, return tuple
        if line.find(';') != -1:
            comp, jump = line.split(';')        # comp ; jump
            dest = "null"
            if comp.find('=') != -1:
                dest, comp = comp.split('=')    # dest = comp ; jump
            parsed = comp, dest, jump
            flag = "C_INSTRUCTION"

        elif line.find('=') != -1:
            dest, comp = line.split('=')        # dest = comp
            jump = "null"
            parsed = comp, dest, jump
            flag = "C_INSTRUCTION"
        else:
            parsed = None
            flag = None

    return parsed, flag


def main(filename):

    try:
        with open(filename, "r") as infile:
            data = infile.readlines()
    except FileNotFoundError:
        print("No such file: \'{}\'\nPlease enter correct filename".format(filename))
        sys.exit(1)

    from instructions import comp, dest, jump

    table = map_table(data)

    machine_code = []

    for line in data:
        parsed, flag = parser(line)
        
        if flag == "A_INSTRUCTION":
            dec = table[parsed]
            bin = dec2bin(dec)
        elif flag == "A_DECIMAL":
            bin = dec2bin(parsed)
        elif flag == "C_INSTRUCTION":
            # Join parsed components from corresponding dictionaries
            # and pad with 1's to match 16 bits of A instruction
            bin = '111' + comp[parsed[0]] + dest[parsed[1]] + jump[parsed[2]]
        else:
            continue

        machine_code.append(bin)

    if not filename.endswith(".asm"):
        filename = filename + ".asm"

    with open(filename.replace(".asm", ".hack"), "w") as outfile:
        outfile.write('\n'.join(machine_code)) # Join each list item with newline

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: assembler <filename>")
        sys.exit(1)

    main(sys.argv[1])

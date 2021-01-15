import sys
import re

def dec2bin(num):
    """Converts a decimal number to binary in string format."""
    bin = ''

    while num != 0:
        quotient = num // 2
        remainder = num % 2
        if remainder == 1:
            bin = '1' + bin
        else:
            bin = '0' + bin
        num = quotient

    bin = '0' + (15 - len(bin)) * '0' + bin # Pad with zeroes to match 16 bits
    return bin


def table_map(asm):
    """Maps the variable names to register addresses."""
    # tableionary of mappings between pre-defined names
    table = {
        "SP"    : 0,
        "LCL"   : 1,
        "ARG"   : 2,
        "THIS"  : 3,
        "THAT"  : 4,
        "SCREEN": 16384,
        "KBD"   : 24576,
        }

    for i in range(0, 16):
        table["R" + str(i)] = i

    # Add user-defined names (i.e. variables and goto's)
    goto_pattern = r'[^\/]*?\(([A-Za-z0-9$._]+)\)'
    var_pattern = r'[^\/]*?@([A-Za-z$_][A-Za-z0-9$._]*)' # all types of variables
    A_pattern = r'[^\/]*?@[0-9]+' # only numerals
    C_pattern = r'[^\/]+?='
    C_pattern2 = r'[^\/=]+?;'

    # First pass for goto
    count = -1
    reg = 16

    var_list = []

    for line in asm:
        goto = re.search(goto_pattern, line)
        var = re.search(var_pattern, line)

        if goto is not None:
            table[goto[1]] = count + 1
        elif re.search(A_pattern, line) is not None:
            count += 1
        elif var is not None:
            var_list.append(var[1])
            count += 1
        elif re.search(C_pattern, line) is not None:
            count += 1
        elif re.search(C_pattern2, line) is not None:
            count += 1

    for i in var_list:
        if table[i] is not None:
            continue
        table[i] = reg
        reg += 1

    return table


def parser(line, table, comp_dict, dest_dict, jump_dict):
    # Remove comment and whitespace
    line = re.sub(r'//.*', '' , line)
    line = line.strip()

    # Find A instruction
    if line.find('@') == 0:
        try:
            dec = int(line[1:])
            bin = dec2bin(dec)
        except:
            dec = table[line]
            bin = dec2bin(dec)
    else:
        if line.find(';') != -1:
            dest, jump = line.split(';')
            comp = "null"
            if dest.find('=') != -1:
                dest, comp = dest.split('=')

        elif line.find('=') != -1:
            dest, comp = line.split('=')
            jump = "null"

        else:
            return None

        comp = comp_dict[comp]
        dest = dest_dict[dest]
        jump = jump_dict[jump]

        # Joining every parts togather
        bin = '111' + comp + dest + jump

    return bin


def main(args):
    with open(args[0]) as asm_file:
        data = asm_file.readlines()

    # Three dictionaries store machine translations for
    # each parts of the C instruction
    comp_dict = {
        "0"  : "0101010",
        "1"  : "0111111",
        "-1" : "0111010",
        "D"  : "0001100",
        "A"  : "0110000",
        "!D" : "0001101",
        "!A" : "0110001",
        "-D" : "0001111",
        "-A" : "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M"  : "1110000",
        "!M" : "1110001",
        "-M" : "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
        }

    dest_dict = {
        "null": "000",
        "M"   : "001",
        "D"   : "010",
        "A"   : "100",
        "MD"  : "011",
        "AM"  : "101",
        "AD"  : "110",
        "AMD" : "111"
        }

    jump_dict = {
        "null": "000",
        "JGT" : "001",
        "JEQ" : "010",
        "JGE" : "011",
        "JLT" : "100",
        "JNE" : "101",
        "JLE" : "110",
        "JMP" : "111"
        }

    table = table_map(data)

    machine_code = []

    for line in data:
        bin = parser(line, table, comp_dict, dest_dict, jump_dict)
        if bin is None:
            continue
        machine_code.append(bin)

    with open(args[1], "w+") as hack_file:
        hack_file.write('\n'.join(machine_code)) # Join each list item with newline


if __name__ == "__main__":
    main(sys.argv[1:])

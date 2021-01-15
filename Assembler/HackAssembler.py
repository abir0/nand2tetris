import sys
import re
import json

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


def json2dict(filename):
    """Converts JSON object into dictoniary."""

    with open(filename) as json_file:
        # Convert the object into dictoniary; file must contain json object
        dict = json.load(json_file)

    if type(dict) == type({}):
        return dict
    else:
        return None


def mapping_dict(asm):
    """Maps the symbolic names to register addresses."""

    dict = {}
    ## Add pre-defined names to the dictoniary
    # Add I/O and VM controll pointers respectively
    dict = {"SCREEN":16384, "KBD":24576, "SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4}
    # Add virtual registers
    for i in range(16):
        dict["R" + str(i)] = i

    ## Now add user-defined names (i.e. variables and goto's)
    goto_pattern = r'[^\/]*?\(([A-Za-z0-9$._]+)\)'
    var_pattern = r'[^\/]*?@([A-Za-z0-9$._]+)' # all types of variables
    A_pattern = r'[^\/]*?@[0-9]+' # only numerals
    C_pattern = r'[^\/]+?='
    C_pattern2 = r'[^\/=]+?;'

    # First pass for goto
    count = -1
    reg = 16

    for line in asm:
        goto = re.search(goto_pattern, line)

        if goto is not None:
            dict[goto[1]] = count + 1
        elif re.search(A_pattern, line) is not None:
            count += 1
        elif re.search(var_pattern, line) is not None:
            count += 1
        elif re.search(C_pattern, line) is not None:
            count += 1
        elif re.search(C_pattern2, line) is not None:
            count += 1

    # Second pass for other variables
    count = -1
    for line in asm:
        var = re.search(var_pattern, line)

        if re.search(A_pattern, line) is not None:
            count += 1
        elif var is not None:
            if dict.get(var[1]) is not None:
                count += 1
                continue
            dict[var[1]] = reg
            reg += 1
            count += 1
        elif re.search(C_pattern, line) is not None:
            count += 1
        elif re.search(C_pattern2, line) is not None:
            count += 1

    return dict


def parser(instruction):
    """Parses a C instruction into binary string format."""

    # Regex for different parts of the instruction
    comp_pattern1 = r'[^\/]*?=([ADM01!&|+-]{1,3})'
    comp_pattern2 = r'[^\/]*?([ADM01!&|+-]{1,3});'
    dest_pattern = r'[^\/]*?([AMD]{1,3})='
    jump_pattern = r'[^\/]*?;([E-T]{3})'

    # Extract each parts
    if re.search(comp_pattern1, instruction) is None:
        comp = re.search(comp_pattern2, instruction)[1]
    else:
        comp = re.search(comp_pattern1, instruction)[1]

    if re.search(dest_pattern, instruction) is None:
        dest = "null"
    else:
        dest = re.search(dest_pattern, instruction)[1]

    if re.search(jump_pattern, instruction) is None:
        jump = "null"
    else:
        jump = re.search(jump_pattern, instruction)[1]

    # Find the corresponding binary valus from JSON file
    filename = 'instruction_table.json'
    dict = json2dict(filename)
    comp = dict["comp"][comp]
    dest = dict["dest"][dest]
    jump = dict["jump"][jump]

    # Joining every parts togather
    binary_code = '111' + comp + dest + jump
    return binary_code


def main(args):
    with open(args[0]) as asm_file:
        asm_data = asm_file.readlines()

    sym_dict = mapping_dict(asm_data)

    Ainstruction_pattern = r'^[^\/]*?@([A-Za-z0-9$._]+)'
    Cinstruction_pattern = r'^[^\/]+?='
    Cinstruction_pattern2 = r'^[^\/=]+?;'

    machine_code = []

    for line in asm_data:
        Ainstruction = re.search(Ainstruction_pattern, line)
        Cinstruction = re.search(Cinstruction_pattern, line)
        Cinstruction2 = re.search(Cinstruction_pattern2, line)

        if  (Cinstruction or Cinstruction2)  is not None:
            bin = parser(line)
            machine_code.append(bin)

        if Ainstruction is not None:
            try:
                dec = int(Ainstruction[1])
            except:
                dec = sym_dict[Ainstruction[1]]

            bin = dec2bin(dec)
            machine_code.append(bin)

    with open(args[1], "w+") as hack_file:
        hack_file.write('\n'.join(machine_code)) # Join each list item with newline


if __name__ == "__main__":
    main(sys.argv[1:])

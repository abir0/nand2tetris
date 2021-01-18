#!/usr/bin/env python3

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
        parsed, flags =  parser(line)
        A_instruction, A_numeric, C_instruction, goto_instruction = flags

        if goto_instruction:
            table[parsed] = count + 1      # add next position after goto
        elif A_numeric:
            count += 1
        elif A_instruction:
            if parsed not in variables_list:
                variables_list.append(parsed)    # append to list if it doesn't exist
            count += 1
        elif C_instruction:
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

    # Flags
    A_instruction = False
    A_numeric = False
    C_instruction = False
    goto_instruction = False

    # Parse A instruction, return int or string
    if line.find('@') == 0:
        try:
            parsed = int(line[1:])
            A_numeric = True
        except:
            parsed = line[1:]
            A_instruction = True

    elif line.startswith("(") and line.endswith(")"):
        parsed = line[1:-1]
        goto_instruction =True
    else:
        # Parse C instruction, return tuple
        if line.find(';') != -1:
            comp, jump = line.split(';')        # comp ; jump
            dest = "null"
            if comp.find('=') != -1:
                dest, comp = comp.split('=')    # dest = comp ; jump
            parsed = comp, dest, jump
            C_instruction = True

        elif line.find('=') != -1:
            dest, comp = line.split('=')        # dest = comp
            jump = "null"
            parsed = comp, dest, jump
            C_instruction = True
        else:
            parsed = None

    flags = A_instruction, A_numeric, C_instruction, goto_instruction
    return parsed, flags


def main(filename):

    try:
        with open(filename, "r") as infile:
            data = infile.readlines()
    except FileNotFoundError:
        print("No such file: \'{}\'\nPlease enter correct filename".format(filename))
        sys.exit(1)
    # Three dictionaries store machine translations for
    # each parts of the C instruction
    comp = {
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

    dest = {
        "null": "000",
        "M"   : "001",
        "D"   : "010",
        "A"   : "100",
        "MD"  : "011",
        "AM"  : "101",
        "AD"  : "110",
        "AMD" : "111"
        }

    jump = {
        "null": "000",
        "JGT" : "001",
        "JEQ" : "010",
        "JGE" : "011",
        "JLT" : "100",
        "JNE" : "101",
        "JLE" : "110",
        "JMP" : "111"
        }

    table = map_table(data)

    machine_code = []

    for line in data:
        parsed, flags = parser(line)
        A_instruction, A_numeric, C_instruction, goto_instruction = flags

        if A_instruction:
            dec = table[parsed]
            bin = dec2bin(dec)
        elif A_numeric:
            bin = dec2bin(parsed)
        elif C_instruction:
            # Join parsed components from corresponding dictionaries
            # and pad with 1's to match 16 bits of A instruction
            bin = '111' + comp[parsed[0]] + dest[parsed[1]] + jump[parsed[2]]
        else:
            continue

        machine_code.append(bin)

    if filename.endswith(".asm"):
        filename = filename.replace(".asm", ".hack")
    else:
        filename = filename + ".hack"

    with open(filename, "w") as outfile:
        outfile.write('\n'.join(machine_code)) # Join each list item with newline


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: assembler <filename>")
        sys.exit(1)

    main(sys.argv[1])

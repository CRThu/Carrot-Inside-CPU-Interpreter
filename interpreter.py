#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import re

INTERPRETER_NAME = 'Carrot Inside CPU Interpreter'
INTERPRETER_INTRODUCTION = 'carrot\'s cpu interpreter for crt4004 and crt8008'
INTERPRETER_VERSION = 'Version 1.4'
INTERPRETER_WEBSITE = 'https://github.com/CRThu/Carrot-Inside-CPU-Interpreter'

# Folder Path
FILE_PATH = "./files/"

# OP
OP_RTYPE = '000000'
OP_LW = '100011'
OP_SW = '101011'
OP_BEQ = '000100'
OP_ADDI = '001000'
OP_NOP = '111111'
OP_SLL = '000010'
OP_SRL = '000011'

# R-TYPE
R_ADD = '100000'
R_SUB = '100010'
R_AND = '100100'
R_OR = '100101'
R_SLT = '101010'

# DEFINE
# _FORMAT_WORD_TO_BYTE_ = False
_FORMAT_BIN_TO_HEX_ = True
_FORMAT_HEX_UPPERCASE_ = True


# Convert '123' to '7b'
def dec_str_to_hex_div4(dec_str):
    return format(math.floor(int(dec_str, 10) / 4), 'x')


# Convert '123' to '01111011' (fill zero)
def dec_str_to_bin(dec_str, bin_len):
    if dec_str[0] == '-' and dec_str != '-0':
        return true_to_complement_dec(dec_str[1:], bin_len)
    else:
        return format(int(dec_str, 10), 'b').zfill(bin_len)


# Convert -4 to '252'
def true_to_complement_dec(dec_str, bin_len):
    return format(pow(2, bin_len) - int(dec_str, 10), 'b').zfill(bin_len)


# ASM to BIN
def asm_interpreter(asm_instr):
    bin_instr = ""
    if asm_instr[0] == 'LOCATE':
        bin_instr = '@' + dec_str_to_hex_div4(asm_instr[1])
    elif asm_instr[0] == 'ADD':
        bin_instr = (OP_RTYPE
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3].replace('$', ''), 5)
                     + '00000' + R_ADD)
    elif asm_instr[0] == 'SUB':
        bin_instr = (OP_RTYPE
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3].replace('$', ''), 5)
                     + '00000' + R_SUB)
    elif asm_instr[0] == 'LW':
        bin_instr = (OP_LW
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'SW':
        bin_instr = (OP_SW
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'BEQ':
        bin_instr = (OP_BEQ
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'ADDI':
        bin_instr = (OP_ADDI
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'SLL':
        bin_instr = (OP_SLL
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'SRL':
        bin_instr = (OP_SRL
                     + dec_str_to_bin(asm_instr[1].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[2].replace('$', ''), 5)
                     + dec_str_to_bin(asm_instr[3], 16))
    elif asm_instr[0] == 'NOP':
        bin_instr = (OP_NOP
                     + '11111'
                     + '11111'
                     + '1111111111111111')
    else:
        bin_instr = '{undefined instruction:' + str(asm_instr) + '}'

    return bin_instr


# split word for bin instructions
def format_bin(instr_str):
    if instr_str[0] == '{' and instr_str[-1] == '}':
        return '*ERROR: ' + instr_str + '*'
    else:
        return instr_str

    # if not _FORMAT_WORD_TO_BYTE_:
    #     return instr_str
    # else:
    #     if instr_str[0] == '@':
    #         return instr_str
    #     elif len(instr_str) == 32:
    #         return instr_str[0:8] + ' ' + instr_str[8:16] + ' ' + instr_str[16:24] + ' ' + instr_str[24:32]
    #     else:
    #         return '*ERROR: {unknown}*'


# convert bin to hex
def format_bin_to_hex(bin_instr):
    if bin_instr[0] == '{' and bin_instr[-1] == '}':
        return bin_instr
    elif bin_instr[0] == '@':
        return bin_instr
    elif len(bin_instr) == 32:
        return format(int(bin_instr, 2), 'X' if _FORMAT_HEX_UPPERCASE_ else 'x').zfill(8)
    else:
        return '*ERROR: {unknown}*'


# split word for hex instructions
def format_hex(instr_str):
    if instr_str[0] == '{' and instr_str[-1] == '}':
        return '*ERROR: ' + instr_str + '*'
    else:
        return instr_str
    # if not _FORMAT_WORD_TO_BYTE_:
    #     return instr_str
    # else:
    #     if instr_str[0] == '@':
    #         return instr_str
    #     if len(instr_str) == 8:
    #         return instr_str[0:2] + ' ' + instr_str[2:4] + ' ' + instr_str[4:6] + ' ' + instr_str[6:8]
    #     else:
    #         return '*ERROR: {unknown}*'


# convert bin to hex & format bin/hex
def format_bin_to_out(instr_bin_str):
    if not _FORMAT_BIN_TO_HEX_:
        return format_bin(instr_bin_str)
    else:
        return format_hex(format_bin_to_hex(instr_bin_str))


class mif_file_gen_class(object):
    # TODO : changing parameters is not supported yet
    def __init__(self, mif_path, mif_width=32, mif_depth=256, addr_radix='HEX', data_radix='HEX'):
        # parameter
        self.mif_path = mif_path
        self.mif_width = mif_width
        self.mif_depth = mif_depth
        self.addr_radix = addr_radix
        self.data_radix = data_radix
        # value
        self.write_mif_file = None
        self.mif_lines = []
        self.rom_addr = 0
        self.append_header()
        self.append_ender()
        self.error_list = []

    def read_lines(self):
        return self.mif_lines

    # write mif file header
    def append_header(self):
        self.mif_lines.append('WIDTH=' + str(self.mif_width) + ';')
        self.mif_lines.append('DEPTH=' + str(self.mif_depth) + ';')
        self.mif_lines.append('')
        self.mif_lines.append('ADDRESS_RADIX=' + self.addr_radix + ';')
        self.mif_lines.append('DATA_RADIX=' + self.data_radix + ';')
        self.mif_lines.append('')
        self.mif_lines.append('CONTENT BEGIN')

    # write instructions
    # '00:FFFFFFFF;'
    def append_instructions(self, bin_instr, instr_line_num):
        if bin_instr[0] == '{' and bin_instr[-1] == '}':  # Known Error
            self.mif_lines.insert(-1, bin_instr)
            self.rom_addr += 1
            self.error_list.append('')
            self.error_list.append('*** ERROR: INTERNAL ERROR FROM ASM INTERPRETER! ***')
            self.error_list.append('*** ' + bin_instr + ' in LINE = ' + str(instr_line_num) + ', PC_WORD = ' + str(
                self.rom_addr) + '. ***')

        elif bin_instr[0] == '@':  # Jump to address
            self.rom_addr = int(bin_instr[1:], 16)

        elif len(bin_instr) == 32:  # Instructions
            self.mif_lines.insert(-1, format(self.rom_addr, 'x').zfill(math.ceil(math.log(self.mif_depth, 16))) + ':'
                                  + format(int(bin_instr, 2), 'X' if _FORMAT_HEX_UPPERCASE_ else 'x').zfill(
                math.ceil(self.mif_width / 8 * 2)) + ';')
            self.rom_addr += 1

        else:  # Unknown Error
            self.mif_lines.insert(-1, '*ERROR: {unknown}*')
            self.rom_addr += 1
            self.error_list.append('')
            self.error_list.append('*** ERROR: UNKNOWN INSTRUCTION! ***')
            self.error_list.append(
                '*** unknown instructions in LINE = ' + str(instr_line_num) + ', PC_WORD = ' + str(
                    self.rom_addr) + '. ***')

    # write mif file end
    def append_ender(self):
        self.mif_lines.append('END;')

    def open(self):
        self.write_mif_file = open(self.mif_path, 'w')

    def close(self):
        self.write_mif_file.close()

    def write_lines(self):
        if self.rom_addr >= self.mif_depth:
            self.error_list.append('')
            self.error_list.append('*** ERROR: INSTRUCTION TO MUCH FOR ROM! ***')
            self.error_list.append(
                '*** PC_WORD(' + str(self.rom_addr) + ') > ROM_DEPTH(' + str(self.mif_depth) + ') ***')

        self.open()
        for mif_line in self.mif_lines:
            self.write_mif_file.write(mif_line + '\n')
        self.close()

        for error_iter in self.error_list:
            print(error_iter)


def main():
    print(INTERPRETER_NAME)
    print(INTERPRETER_INTRODUCTION)
    print(INTERPRETER_VERSION)
    print(INTERPRETER_WEBSITE)
    print()

    # read input file name
    try:
        asm_path = FILE_PATH + sys.argv[1]
    except IndexError:
        asm_path = FILE_PATH + 'rom_raw.asm'

    # read input asm file name
    if asm_path.rfind('.asm') == -1:
        asm_path += '.asm'

    # generate output dat file name
    dat_path = asm_path.replace('.asm', '.dat')

    # generate output mif file name
    mif_path = asm_path.replace('.asm', '.mif')

    print('input  asm path:\t' + asm_path)
    print('output dat path:\t' + dat_path)
    print('output mif path:\t' + mif_path)
    print()

    # read asm file
    read_asm_file = open(asm_path)

    # preprocess
    asm_instr_list = [re.sub(r'[\r\n\t]', '', i) for i in read_asm_file.readlines()]  # delete ctrl characters
    while '' in asm_instr_list:
        asm_instr_list.remove('')
    asm_instr_list = [re.sub(r'\s+', ' ', i) for i in asm_instr_list]  # delete spaces
    asm_instr_list = [i.split(';')[0].strip() for i in asm_instr_list]  # delete annotations

    read_asm_file.close()

    for asm_instr in asm_instr_list:
        if asm_instr == '':
            asm_instr_list.remove(asm_instr)

    print('raw list:\t', end='')
    print(asm_instr_list)

    # split instruction
    asm_instr_element_list = [re.split(r'[^0-9|a-z|A-Z|$|-]+', i) for i in asm_instr_list]  # split elements

    print('asm list:\t', end='')
    print(asm_instr_element_list)

    # interpreter to asm
    bin_instr_list = [asm_interpreter(asm_instr) for asm_instr in asm_instr_element_list]
    # output format
    out_instr_list = [format_bin_to_out(bin_instr) for bin_instr in bin_instr_list]

    print('%s list:\t' % ('bin' if not _FORMAT_BIN_TO_HEX_ else 'hex'), end='')
    print(out_instr_list)

    # write dat file
    write_dat_file = open(dat_path, 'w')
    for i in out_instr_list:
        write_dat_file.write(i + '\n')
    write_dat_file.close()

    # write mif file
    mif_file_gen = mif_file_gen_class(mif_path)

    iter_index = 0
    for bin_instr in bin_instr_list:
        iter_index += 1
        mif_file_gen.append_instructions(bin_instr, iter_index)

    print('mif list:\t', end='')
    print(mif_file_gen.read_lines())

    mif_file_gen.write_lines()


if __name__ == '__main__':
    main()

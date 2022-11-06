#!/usr/bin/env python
#
#  Name: r2_metaData_extractor.py
#  Description: A script that will get from one binary file it's metadata


import sys
import argparse
import os

try:
    import r2pipe
    from itanium_demangler import parse as demangle
except ImportError as err:
    print("Error while importing module: %s" % str(err))
    sys.exit(0)



FUNCS_PREFIX_EXCLUD = ["sym._GLOBAL__sub_I_"]



def save_data(dir , filename , metadata , type  = 'raw'):
    filename = filename + '.' + type
    file_path = os.path.join(dir, filename)
    with open(file_path, 'w') as file:
        file.write(metadata)
    pass


def my_demangle(mangled_func_name):


    if demangle(mangled_func_name) != None:
        mangled_func_name = demangle(mangled_func_name)


    if len(mangled_func_name) > 255: # too long name for save in OS filesystem. try some cut
        rem_words = ["_void_", "const_", "volatile_", "_anonymous_namespace_::", "_unsigned_", "long_", "_int_", "_const", "cxx11_", "message_abi:",
                     "_char_", "_unsigned_long_" ]
        for word in rem_words:
            mangled_func_name = mangled_func_name.replace(word, "")
            mangled_func_name.strip("_")
            if len(mangled_func_name) < 255:
                break

    if len(mangled_func_name) > 255:
        return mangled_func_name[:250] # + 5 symbols for  .json

    return mangled_func_name


def main():
    parser = argparse.ArgumentParser(description='Extract from binary all function metadata .')
    parser.add_argument('-i', '--inputFile', required=True, type=str, help='path to binary.')
    parser.add_argument('-o',  '--outputDir',  type=str, help='dir to save extracted metadata. Default save to currient dir.')
    args = parser.parse_args()

    cur_dir = os.path.dirname(__file__) # default
    if args.outputDir:
        cur_dir = args.outputDir

    r2 = r2pipe.open(args.inputFile)
    r2.cmd('aa')

    funcs_name = [funcs_line.strip().split()[3] for funcs_line in r2.cmd("afl").split("\n") if len(funcs_line) > 0]
    funcs_addresses = [funcs_line.strip().split()[0] for funcs_line in r2.cmd("afl").split("\n") if len(funcs_line) > 0]

    i = 0
    for cur_fun in funcs_name:
        if cur_fun[:19] not in  FUNCS_PREFIX_EXCLUD:
            func_clear_name = my_demangle(cur_fun)
            r2.cmd("s {0}".format(funcs_addresses[i]))
            asm_code = r2.cmd("pif")
            cfg_agfg = r2.cmd("agfg")
            asm_all = r2.cmd("agfj")
            # other metadata extractions appends here

            save_data(dir=cur_dir, filename=func_clear_name, metadata=cfg_agfg, type='gml')
            save_data(dir=cur_dir, filename=func_clear_name, metadata=asm_code)
            save_data(dir=cur_dir, filename=func_clear_name, metadata=asm_all, type='json')
        i+=1



if __name__ == "__main__":
    main()
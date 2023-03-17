#!/usr/bin/env python
#
#  Name: r2_metaData_extractor.py
#  Description: A script that will get from one binary file it's metadata


import sys
import argparse
import os


try:
    import r2pipe
    import hashlib
    from itanium_demangler import parse as demangle
except ImportError as err:
    print("Error while importing module: %s" % str(err))
    sys.exit(0)










FUNCS_PREFIX_EXCLUD = ["sym._GLOBAL__sub_I_"]



def save_data(dir , filename , metadata , type  = 'raw', flag = 'w'):
    filename = filename + '.' + type
    file_path = os.path.join(dir, filename)
    with open(file_path, flag) as file:
        file.write(metadata)
    pass


def my_demangle(mangled_func_name):


    if demangle(mangled_func_name) != None:
        mangled_func_name = demangle(mangled_func_name)


    if len(mangled_func_name) > 255: # too long name for save in OS filesystem. try some cut
        rem_words = ["_void_", "const_", "volatile_", "_anonymous_namespace_::", "_unsigned_", "long_", "_int_", "_const", "cxx11_", "message_abi:",
                     "_char_", "_unsigned_long_", "basic_string_char_" , "char_traits_char_" , "_______", "_unsigned_long_", "allocator_std"]
        for word in rem_words:
            mangled_func_name = mangled_func_name.replace(word, "")
            mangled_func_name.strip("_")
            if len(mangled_func_name) < 255:
                break

    if len(mangled_func_name) > 255:
        return mangled_func_name[:250] # + 5 symbols for  .json

    return mangled_func_name


def hash_the_func(mangled_func_name):
    if demangle(mangled_func_name) != None:
        mangled_func_name = demangle(mangled_func_name)

    md5 = hashlib.md5(mangled_func_name.encode())
    return(md5.hexdigest())


def main():
    parser = argparse.ArgumentParser(description='Extract from binary all function metadata .')
    parser.add_argument('-i', '--inputFile', required=True, type=str, help='path to binary.')
    parser.add_argument('-o',  '--outputDir',  type=str, help='dir to save extracted metadata. Default save to currient dir.')
    parser.add_argument('-f', '--fileHashDir', type=str,
                        help='Dir to save original and hashed func\'s name in file hashedNames.txt. Default  - don\'t save.')
    args = parser.parse_args()

    cur_dir = os.path.dirname(__file__) # default
    if args.outputDir:
        cur_dir = args.outputDir

    r2 = r2pipe.open(args.inputFile,  ["-e bin.cache=true"]) # For disable stderr messages use flags=['-2']
    r2.cmd('aa')

    funcs_name = [funcs_line.strip().split()[3] for funcs_line in r2.cmd("afl").split("\n") if len(funcs_line) > 0]
    funcs_addresses = [funcs_line.strip().split()[0] for funcs_line in r2.cmd("afl").split("\n") if len(funcs_line) > 0]

    i = 0
    for cur_fun in funcs_name:
        if cur_fun[:19] not in  FUNCS_PREFIX_EXCLUD:
            func_clear_name = hash_the_func(cur_fun)
            r2.cmd("s {0}".format(funcs_addresses[i]))
            asm_code = r2.cmd("pif")
            cfg_agfg = r2.cmd("agfg")
            asm_all = r2.cmd("agfj")
            # other metadata extractions appends here

            save_data(dir=cur_dir, filename=func_clear_name, metadata=cfg_agfg, type='gml')
            save_data(dir=cur_dir, filename=func_clear_name, metadata=asm_code)
            save_data(dir=cur_dir, filename=func_clear_name, metadata=asm_all, type='json')
            if args.fileHashDir:
                save_data(dir=args.fileHashDir, filename="hashedNames", metadata="{}\t{}\n".format(func_clear_name,cur_fun ), type='txt',flag='a')
        i+=1

    r2.quit()


class WTF:
        ''' 
    Class: What does this func do? 
    '''
        def __init__(self, binary_file = None, path_to_binary_file = "...") -> None:
            if (binary_file == None) and (path_to_binary_file == "..."):
                print("Not setted file to analyse!")
                exit(0)
            if path_to_binary_file != "...":
                #print("TRY: {}".format(os.path.join(os.path.dirname(__file__), path_to_binary_file)))
                self.__path_to_file = os.path.join(os.path.dirname(__file__), path_to_binary_file)
                #print("TRY: {}".format(self.__path_to_file))
                self.__r2 = r2pipe.open( self.__path_to_file , ["-e bin.cache=true"])

            else:
                #self.__r2 = r2pipe.open()
                self.__r2 = r2pipe.open(binary_file)

            self.__r2.cmd('aa')
            self.__funcs_names = []
            self.__funcs_addresses = []

        def __get_funcs_names(self):
            self.__funcs_names = [funcs_line.strip().split()[3] for funcs_line in self.__r2.cmd("afl").split("\n") if len(funcs_line) > 0]


        def __get_funcs_addresses(self):
            self.__funcs_addresses = [funcs_line.strip().split()[0] for funcs_line in self.__r2.cmd("afl").split("\n") if len(funcs_line) > 0]


        async def get_functions_count(self):
            if self.__funcs_names == []:
                self.__get_funcs_names()
            return len(self.__funcs_names)

        async def get_functions_names(self):
            if self.__funcs_names == []:
                self.__get_funcs_names()
            return self.__funcs_names
        

        async def get_functions_asm_code(self, get_the_graph = False):
            """
            return dictionary of list {"real_func_name": ["raw_code", "cfg"]}
            example : return  {"boost::set_params<bool>": ["POP PUSH ADD...", "[1] [1-3]...."]}
            """
            if self.__funcs_names == []:
               self.__get_funcs_names()
            if self.__funcs_addresses == []:
               self.__get_funcs_addresses()
            
            funcs = {}
            cfg_agfg = ""

            i = 0   
            for cur_fun in self.__funcs_names:
                if cur_fun[:19] not in  FUNCS_PREFIX_EXCLUD:
                    func_clear_name = hash_the_func(cur_fun)
                    self.__r2.cmd("s {0}".format(self.__funcs_addresses[i])) 
                    asm_code = self.__r2.cmd("pif") # get asm raw code
                    if get_the_graph:
                        cfg_agfg = self.__r2.cmd("agfg") # get asm cfg

                    funcs[func_clear_name] = [asm_code, cfg_agfg]
                i+=1
            return funcs

        def __del__(self):
            # body of destructor
            try:
                self.__r2.quit()
            except:
                pass



if __name__ == "__main__":
    main()
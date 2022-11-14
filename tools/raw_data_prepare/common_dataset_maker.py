import numpy as np
import os


def get_name_by_hash(hashed_name):
    return "name_TODO" # TODO: get func name by hash


def get_clas_by_module(module_name):
    return "class_TODO" # TODO add class selection here


def list_files(startpath):

    library = ""
    bin = "elf"
    compiller = ""
    version = ""
    compiler_option = ""
    func_class = ""
    func_name = ""
    func_hash_name = ""
    instructions_count = ""
    func_body = ""
    func_graph = ""


    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)

        if level == 1:
            library =  os.path.basename(root)

        if level == 2:
            compiller_list = str(os.path.basename(root)).split("_")
            compiller = compiller_list[0]
            version = compiller_list[1]
            compiler_option = compiller_list[2]

        if level == 3:
            func_class = get_clas_by_module(os.path.basename(root))


            for f in files:

                if f[-4:] == ".raw":
                    func_name = get_name_by_hash(f[:-4])

                    with open(root+os.sep+f) as fl:
                        func_body = fl.readlines()
                    instructions_count = len(func_body)
                    func_body = [elem.strip("\n") for elem in func_body]

                    #with open(root+os.sep+f[:-4]+".gml") as fl:
                    #    func_graph = fl.readlines()

                    print(library, compiller,version, compiler_option, func_class, func_name, f[:-4],instructions_count, func_body, func_graph )



list_files("../../raw_data")

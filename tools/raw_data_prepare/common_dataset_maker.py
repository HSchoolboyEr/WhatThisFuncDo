import numpy as np
import os
import pandas as pd

real_func_names = np.loadtxt("../../raw_data/hashedNames.txt" , dtype="str",  delimiter='\t')
classes= np.loadtxt("../../raw_data/boost/classes_mapping.txt" , dtype="str",  delimiter=':')
file_to_save_result = '../../data/extracted.csv'




def get_name_by_hash(hashed_name):
    result = np.where((real_func_names[0:, 0] == hashed_name))
    if not result:
        return (real_func_names[result[0], 1][0])
    else:
        return("too_dificult_hash")


def get_clas_by_module(module_name):
    result = np.where((classes[0:, 0] == module_name))
    if (result[0].size == 0):
        return "Another"
    return(classes[result[0], 1][0])


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
    column_names = ['library', 'bin', 'compiller',  'version' ,
                    'compiler_option', 'func_class' , 'func_name',
                    'name_hash','instructions_count', 'func_body' ,
                    'func_graph']

    first = True

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

            counter = 0
            for f in files:
                if f[-4:] == ".raw":
                    func_name = get_name_by_hash(f[:-4])

                    with open(root+os.sep+f) as fl:
                        func_body = fl.readlines()
                    instructions_count = len(func_body)
                    func_body = str([elem.strip("\n") for elem in func_body])

                    #with open(root+os.sep+f[:-4]+".gml") as fl:
                    #    func_graph = fl.readlines()

                    list_line = np.array([[library], [bin], [compiller], [version],[compiler_option],
                                          [func_class], [func_name], [f[:-4]], [instructions_count], [func_body], [func_graph]]).T

                    if first:
                        pdArrayLine = pd.DataFrame(list_line, columns=column_names)
                        pdArrayLine.to_csv(file_to_save_result, sep=';', index=False)
                        first = False
                    else:
                        pdArrayLine = pd.DataFrame(list_line)
                        pdArrayLine.to_csv(file_to_save_result, sep=';', mode='a', index=False, header=False)
                    counter+=1
                    if counter % 1000 == 0:
                        print(counter)


list_files("../../raw_data")

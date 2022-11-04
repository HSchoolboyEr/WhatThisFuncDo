# Getting Started

All scripts for data preparation are located in this folder

## Using 

*Requirements*: Python 3 (with r2pipe), radare2


First you need to prepare the binaries on your computer according to the instructions of the libraries you have selected 


Then you can use the `r2_metaData_extractor.py` to get the required metadata from one binary:
```
python3.9 r2_metaData_extractor.py -i /path/to/binary/file.o -o /path/to/folder/for/save/result
```

*For this time* it extract only assm code, flow grapf (in format Graph Modelling Language https://gephi.org/users/supported-graph-formats/gml-format/) and all the data in JSON


If you neen more files, use the `boost_tree_walker.sh` for recursive walking by library's folders.

*For this time* it use boost (https://www.boost.org/) folders structure and only Linux *.o binary


## ToDo


* Add more libraries

* Prepare (trim, strip, normalize and ather) all the data from forlder `raw_data`

* Work with funcs name and folders structure
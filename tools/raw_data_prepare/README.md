# Getting Started  to prepare data

All scripts for data preparation are located in this folder

In this section decribed how to prepare the existed data or add new. If you wont to use already preparead data - go to `./data/`  [folder](../../data/) of this repo.

## Using 

*Requirements*: Python 3 (with r2pipe, itanium_demangler), radare2



### Step 1

First you need to prepare the binaries on your computer according to the instructions of the libraries you have selected 

It is highly desirable to compile several libraries with several  optimization options (for example, standard O0, O1 and O2) and different compilers and their versions. This may allow you to create slightly different code for the same function in some of its places. The various options must be placed in a separate folder in the main folder with the name of the library in the form of "Compiler_version_option". For example, `./raw_data/boost/gcc_10_O1/`. Saving data in this form will make it easy to supplement new data and easily use the script `raw_data_aggregator.sh ` to collect them into a single file in the ./data/ folder.

My Boost's native [b2](https://www.bfgroup.xyz/b2/) compile-setting file is also here: `boost_project-config.jam`

*Note* The GCC v4.7 has 2^82 possible optimization combinations...see [there](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)

### Step 2

Then you can use the `r2_metaData_extractor.py` to get the required metadata from one binary:
```
$python r2_metaData_extractor.py -i /path/to/binary/file.o -o /path/to/folder/for/save/result
```

*For this time* it extract only:
* disasm code
* flow grapf (in format [Graph Modelling Language](https://gephi.org/users/supported-graph-formats/gml-format/))
* all the data in JSON

During extract metadata sometimes it's necessary to de-mangle function's names. The easiest way  - use `c++filt` or python packeges ([cxxfilt](https://github.com/afq984/python-cxxfilt) or [itanium_demangler](https://github.com/whitequark/python-itanium_demangler)), but in my way it isn't always works correctly. I use it in func `my_demangle`.

*Note* (https://en.wikipedia.org/wiki/Name_mangling): 
>"Because C++ symbols are routinely exported from DLL and shared object files, the name mangling scheme is not merely a compiler-internal matter. Different compilers (or different versions of the same compiler, in many cases) produce such binaries under different name decoration schemes, meaning that symbols are frequently unresolved if the compilers used to create the library and the program using it employed different schemes. For example, if a system with multiple C++ compilers installed (e.g., GNU GCC and the OS vendor's compiler) wished to install the Boost C++ Libraries, it would have to be compiled multiple times (once for GCC and once for the vendor compiler)".

Boost in default use a generic source file dummy_demangler.cpp. If you know about this ABI dialect, please, write me: `dlmalloc_allocation_command_unsigned_int__unsigned_long__unsigned_long__unsigned_long__unsigned_long__void_` 

### Step 3 
If you neen more files, use the `boost_tree_walker.sh` for recursive walking by library's folders.

*For this time* it use [boost](https://www.boost.org/) folders structure and only Linux *.o binary. But most Boost libraries are header-only: they consist entirely of header files containing templates and inline functions, and require no separately-compiled library binaries or special treatment when linking.


## ToDo

- [x] demangle [ABI](https://en.wikipedia.org/wiki/Application_binary_interface)
- [x] control function's names len
- [ ] Add more libraries
- [ ] Prepare (trim, strip, normalize and ather) all the data from forlder `raw_data`
- [ ] Create script `raw_data_aggregator.sh `
- [ ] Work with funcs name and folders structure
- [ ] Check the size if func: short funcs doesn't need



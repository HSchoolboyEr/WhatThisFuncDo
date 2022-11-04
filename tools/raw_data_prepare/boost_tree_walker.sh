#!/bin/bash

cur_lib=""
prefix_lib="/home/user/boost/binary2/boost/bin.v2/libs"
lib_into_path="/build/gcc-10/release/link-static/"

prefix_proj="/home/user"
path_to_save=$prefix_proj"/WhatThisFuncDo/raw_data/boost/"



recurse() {
 for i in "$1"/*;do
    if [ -d "$i" ];then
	    cur_lib=$(echo "$i" | awk -F/ '{print $NF}')
            echo "===================LIB: $cur_lib"
        recurse_deep	"$i$lib_into_path"
    fi
 done
}

recurse_deep(){
 for i in "$1"/*;do
    if [ -d "$i" ];then
        recurse_deep "$i"
    elif [ -f "$i" ]; then
        if [[ $i == *.o ]];then
		echo "$i" | awk -F "/" '{print $NF}'
		if [ ! -d "$path_to_save$cur_lib" ]; then
  			mkdir -p "$path_to_save$cur_lib";
		fi
		$(python3.9 $path_to_save'../../tools/raw_data_prepare/r2_metaData_extractor.py' -i $i -o $path_to_save$cur_lib)
	fi
    fi
 done
}

recurse $prefix_lib

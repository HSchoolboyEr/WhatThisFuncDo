#!/bin/bash


LIB='boost'
COMPILER='gcc'
#COMPILER_VER='10.2.1'
#COMPILER_OPTION='O0'







for COMPILER_VER in  "10.2.1" "9.3.0"; do
  for COMPILER_OPTION in  "O0" "O1" "O2" "O3" "Os" "Og" "Ofast";do

        COMPILER_CONF=$COMPILER"_"$COMPILER_VER"_"$COMPILER_OPTION
        prefix_lib="/home/user/boost/binary_"$COMPILER_CONF"/boost/bin.v2/libs"
        lib_into_path="/build/"$COMPILER"-"$COMPILER_VER"/release/link-static/"
        path_to_save="../../raw_data/$LIB/$COMPILER_CONF/"


        cur_module=""
        recurse() {
         for i in "$1"/*;do
            if [ -d "$i" ];then
              cur_module=$(echo "$i" | awk -F/ '{print $NF}')
                    echo "===================LIB: $cur_module"
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
            if [ ! -d "$path_to_save$cur_module" ]; then
                mkdir -p "$path_to_save$cur_module";
            fi
            $(python3.9 r2_metaData_extractor.py -i $i -o "$path_to_save$cur_module")
          fi
            fi
         done
        }
        recurse $prefix_lib
  done
done